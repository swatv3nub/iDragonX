# https://greentreesnakes.readthedocs.io/
import re
import ast
import sys
import html
import inspect
import asyncio
from io import StringIO, BytesIO
from pyrogram import filters
from iDragonX import app, session, CMD_HELP
from config import PREFIX
from sqlalchemy.future import select

exec_tasks = dict()

class SessionProxy:
	def __init__(self, thing=None):
		self.thing = thing
	def __getattr__(self, attr):
		return getattr(self.thing, attr)
	def __bool__(self):
		return bool(self.thing)
	def __repr__(self):
		return repr(self.thing)
	def __str__(self):
		return str(self.thing)
	def __iter__(self):
		yield iter(self.thing)
	def __call__(self, *args, **kwargs):
		return self.thing(*args, **kwargs)
	def get_thing(self):
		return self.thing
	def set_thing(self, thing):
		self.thing = thing
		
session = SessionProxy()
session_factory = SessionProxy()

PYEXEC_REGEX = '^(?:' + '|'.join(map(re.escape, PREFIX)) + r')exec\s+([\s\S]+)$'
@app.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.regex(PYEXEC_REGEX))
async def pyexec(client, message):
    match = re.match(PYEXEC_REGEX, message.text.markdown)
    if not match:
        return
    code = match.group(1).strip()
    class UniqueExecReturnIdentifier:
        pass
    tree = ast.parse(code)
    obody = tree.body
    body = obody.copy()
    body.append(ast.Return(ast.Name('_ueri', ast.Load())))
    def _gf(body):
        # args: c, client, m, message, executing, r, reply, _ueri
        func = ast.AsyncFunctionDef('ex', ast.arguments([], [ast.arg(i, None, None) for i in ['c', 'client', 'm', 'message', 'executing', 'r', 'reply', 'session', 's', 'session_factory','sf', 'select', '_ueri']], None, [], [], None, []), body, [], None, None)
        ast.fix_missing_locations(func)
        mod = ast.parse('')
        mod.body = [func]
        fl = locals().copy()
        exec(compile(mod, '<ast>', 'exec'), globals(), fl)
        return fl['ex']
    try:
        exx = _gf(body)
    except SyntaxError as ex:
        if ex.msg != "'return' with value in async generator":
            raise
        exx = _gf(obody)
    reply = await message.reply_text(f'Executing <code>{hash(UniqueExecReturnIdentifier)}</code>...')
    oasync_obj = exx(client, client, message, message, reply, message.reply_to_message, message.reply_to_message, session, session, session_factory, session_factory, select, UniqueExecReturnIdentifier)
    if inspect.isasyncgen(oasync_obj):
        async def async_obj():
            return [i async for i in oasync_obj]
    else:
        async def async_obj():
            to_return = [await oasync_obj]
            return [] if to_return == [UniqueExecReturnIdentifier] else to_return
    stdout = sys.stdout
    stderr = sys.stderr
    wrapped_stdout = StringIO()
    wrapped_stderr = StringIO()
    try:
        sys.stdout = wrapped_stdout
        sys.stderr = wrapped_stderr
        task = asyncio.create_task(async_obj())
        exec_tasks[hash(UniqueExecReturnIdentifier)] = task
        returned = await task
    except asyncio.CancelledError:
        sys.stdout = stdout
        sys.stderr = stderr
        exec_tasks.pop(hash(UniqueExecReturnIdentifier), None)
        await reply.edit_text('Cancelled')
        return
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
        exec_tasks.pop(hash(UniqueExecReturnIdentifier), None)
    wrapped_stderr.seek(0)
    wrapped_stdout.seek(0)
    output = ''
    wrapped_stderr_text = wrapped_stderr.read().strip()
    wrapped_stdout_text = wrapped_stdout.read().strip()
    if wrapped_stderr_text:
        output += f'<code>{html.escape(wrapped_stderr_text)}</code>\n'
    if wrapped_stdout_text:
        output += f'<code>{html.escape(wrapped_stdout_text)}</code>\n'
    for i in returned:
        output += f'<code>{html.escape(str(i).strip())}</code>\n'
    if not output.strip():
        output = 'Executed'
    
    # send as a file if it's longer than 4096 bytes
    if len(output) > 4096:
        out = wrapped_stderr_text + "\n" + wrapped_stdout_text + "\n"
        for i in returned:
            out += str(i).strip() + "\n"
        f = BytesIO(out.strip().encode('utf-8'))
        f.name = "output.txt"
        await reply.delete()
        await message.reply_document(f)
    else:
        await reply.edit_text(output)

@app.on_message(~filters.forwarded & ~filters.sticker & ~filters.via_bot & ~filters.edited & filters.me & filters.command(['cancelexec', 'cexec'], prefixes=PREFIX))
async def cancelexec(client, message):
    try:
        task = exec_tasks.get(int(message.command[1]))
    except IndexError:
        return
    if not task:
        await message.reply_text('Task does not exist')
        return
    task.cancel()
    
CMD_HELP.update(
    {
        "Exec": f"""
『 **• Exec** 』
  `{PREFIX}exec` -> Executes python code!
  `{PREFIX}cexec` -> Cancel exec task!
  `{PREFIX}sh` -> Run Commands in shell!
  `{PREFIX}eval` -> For Pyrogram!
  `{PREFIX}evalx` -> For Telethon!
"""
    }
)
