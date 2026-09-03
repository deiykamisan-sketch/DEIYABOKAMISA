"""Arabic and English voice-command parser."""
COMMANDS={'clear':['امسح السبورة','clear board'],'red':['غير اللون للأحمر','color red'],'blue':['غير اللون للأزرق','color blue'],
          'bigger':['كبر القلم','bigger pen'],'undo':['تراجع','undo'],'save':['احفظ الصفحة','save page'],'record':['ابدأ التسجيل','start recording']}
def parse_command(text):
    normalized=' '.join(text.lower().split())
    return next((name for name,phrases in COMMANDS.items() if any(p in normalized for p in phrases)),None)
