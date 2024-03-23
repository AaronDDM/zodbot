
import discord
from discord.ext import commands
from zodbot.vector_db import vector_db
from zodbot.db import db


class Vectors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="migrate_db")
    async def migrate_db(self, ctx: commands.Context, version: int):
        # Say we're migrating the database
        await ctx.send("Migrating database...")

        # Migrate the database
        db.migration(version)

        await ctx.send("Database migrated")

    @commands.command(name="search")
    async def search(self, ctx: commands.Context, message: str):
        # Say we're searching for the message
        await ctx.send("Searching for message: {}".format(message))

        # Search for the most similar messages
        results = vector_db.search(message, 5)

        # Lookup the ids in the database
        for result in results:
            uids = [r["id"] for r in result]
            messages = db.get_messages_by_ids(uids)

            # Send the results to the user
            embed = discord.Embed(title="Results")

            for message in messages:
                embed.add_field(name="User", value=f"<@{message["uid"]}>", inline=False)
                embed.add_field(name="Message", value=message["message"], inline=False)

            await ctx.send(embed=embed)

    @commands.command(name="reset_database")
    async def reset_database(self, ctx: commands.Context):
        # Say we're resetting the database
        await ctx.send("Resetting database...")

        # Reset the database
        vector_db.reset_database()
        
        await ctx.send("Database reset")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot
        if message.author == self.bot.user:
            return
        
        # Ensure the message isn't a command
        if message.content.startswith(self.bot.command_prefix):
            return
        
        # Add the message to the database
        message_id = db.add_message(message.author.id, message.content)
        
        # Add the message to the vector database
        vector_db.insert(message_id, message.content)
        