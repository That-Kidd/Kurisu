from inspect import signature
from typing import TYPE_CHECKING
from . import OptionalMember

if TYPE_CHECKING:
    from discord import Member
    from discord.ext.commands import Context
    from kurisu2 import Kurisu2
    from . import MemberOrID


def caller_as_default(func):
    """Return the command caller for the member argument if none was provided."""
    async def decorator(self, ctx: 'Context', member: 'Member' = None, *args, **kwargs):
        if member is None:
            member = ctx.message.author
        return await func(self, ctx, member, *args, **kwargs)
    decorator.__signature__ = signature(func)
    decorator.__annotations__ = func.__annotations__
    decorator.__name__ = func.__name__
    decorator.__doc__ = func.__doc__
    return decorator


def caller_id_as_default(func):
    """Return the command caller for the member argument if none was provided."""
    async def decorator(self, ctx: 'Context', member: 'MemberOrID' = None, *args, **kwargs):
        if member is None:
            member = OptionalMember(ctx.message.author.id, ctx.message.author)
        return await func(self, ctx, member, *args, **kwargs)
    decorator.__signature__ = signature(func)
    decorator.__annotations__ = func.__annotations__
    decorator.__name__ = func.__name__
    decorator.__doc__ = func.__doc__
    return decorator


class Extension:
    """Base class for Kurisu2 extensions."""

    def __init__(self, bot: 'Kurisu2'):
        """Initialize the extension."""
        bot.log.debug('Initializing extension %s', type(self).__name__)

        self.bot = bot
        self.log = bot.log

        self.restrictions = bot.restrictions
        self.warns = bot.warns
        self.configuration = bot.configuration
