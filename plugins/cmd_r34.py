from plugins.main import *

command = Commands()
command.servers = [ config[ "thecult" ][ "ID" ], config[ "testserver" ][ "ID" ] ]
command.information = '''
Re-post a random image from https://rule34.us

- r34 page=``page number``, tags=``tags names``

In case of repeated post react with ❌ within 30 seconds to remove it.
'''
command.function = 'on_command'

RegisterCommand( plugin_name='cmd_r34', command_name='r34', command_class=command );

def get_r34_post( tags : list, page ):

    for i, t in enumerate( tags ):
        tags[i] = t.strip( ' ' );

    tag_string = '+'.join(tags)
    tag_string = f'{tag_string}&page={page}'

    url = f'https://rule34.us/index.php?r=posts/index&q={tag_string}'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup( response.text, 'html.parser' )

    posts = soup.find_all('div', style='border-radius: 3px; margin: 0px 10px 15px 10px; overflow: hidden; height: 200px; ')

    if not posts:
        return None

    random_post = random.choice( posts )

    image_page_url = random_post.find( 'a' )[ 'href' ]

    image_page_response = requests.get( image_page_url )

    if image_page_response.status_code != 200:
        return None

    image_page_soup = BeautifulSoup(image_page_response.text, 'html.parser')

    if image_page_soup is None:
        return None

    content_push = image_page_soup.find( 'div', class_='content_push' )

    image_url = content_push.find( 'img' )[ 'src' ]

    if not image_url or image_url == 'v1/icons/heart-fill.svg': # Try video

        image_url = content_push.find( 'source', type="video/webm" )[ 'src' ]

    return image_url

async def on_command( message: discord.Message, arguments: dict ):

    tags = arguments[ "tags" ].split( ' ' ) if 'tags' in arguments else [];

    url = get_r34_post( tags, 0 if not 'page' in arguments else arguments[ 'page' ] );

    if url:

        media: discord.Message = await message.channel.send(url);

        await media.add_reaction('❌');

        await asyncio.sleep( 30 );

        media = await media.channel.fetch_message( media.id );

        for reaction in media.reactions:

            if str(reaction.emoji) == '❌':

                users = await reaction.users().flatten();

                if len(users) > 1:

                    await media.delete();

                    return

                else:

                    await media.clear_reactions();
