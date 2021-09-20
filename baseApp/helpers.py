from django.utils.translation import activate, get_language_info
active_laguage = ['ar' ,'fr']
def prepare_lang(lang_code):
    if lang_code not  in active_laguage :
        lang_code = 'ar'
    activate(lang_code)
    return lang_code
 
