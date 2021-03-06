import goslate
import emoji
from emoji import get_emoji_regexp
from userbot.events import register


@register(outgoing=True, pattern="^.gs(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        # https://t.me/c/1220993104/192075
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = "en"
    else:
        await event.edit("`.gs LanguageCode` as reply to a message")
        return
    roman = goslate.Goslate(text) 
    language_id = roman.detect(text)
    src_lan = roman.get_languages()[language_id]
    
    roman_gs = goslate.Goslate(writing=goslate.WRITING_ROMAN)
    text = emoji.demojize(text.strip())
#    script = roman_gs.translate(text, lan)  
    try:
        scripted = roman_gs.translate(text, lan)
        after_gs_text = scripted.text
        mono_gs_text = (("`{}`").format(after_gs_text))
        # TODO: emojify the :
        # either here, or before translation
        output_str = """**ROMANISED** from {} to {}
{}""".format(
            src_lan,
            lan,
            mono_gs_text
        )
        
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))

