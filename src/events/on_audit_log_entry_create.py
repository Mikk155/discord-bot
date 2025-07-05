from project import *;

@bot.event
async def on_audit_log_entry_create( entry: discord.audit_logs.AuditLogEntry ):

    try:

        await g_PluginManager.CallFunction( "OnAuditLog", entry, Guild=entry.guild );

    except Exception as e:

        bot.HandleException( e, SendToDevs=True );
