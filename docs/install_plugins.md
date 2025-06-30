# Installing

- Drop the `.py` file inside `plugins/`

- open [config/plugins.json](/config/plugins.json) and add the plugin filename following the schema instructions

```json
{
    "$schema": "../schemas/plugins.json",

    "ping_counter": {},
    "member_say": {}
}
```

Some may come with extra files. they should always be placed in within the `plugins/` folder.
