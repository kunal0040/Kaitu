from .aliases import COMMAND_ALIASES, TARGET_ALIASES, normalize_target

from .app_discovery import get_installed_apps, get_running_process, close_application

from .command_engine import (
    load_personal_webpages, 
    open_application, 
    search_web, 
    detect_command, 
    execute_command
)

from .commands import (
    LOCAL_RESPONSES, 
    LOCAL_PHRASES, 
    WAKE_WORDS, 
    TWO_WAY_VOICE_COMMAND, 
    TEXT_TO_SPEECH_COMMAND, 
    VOICE_INPUT_COMMAND, 
    RETURN_TO_TEXT_COMMAND, 
    SWITCH_TO_FEMALE_COMMAND, 
    SWITCH_TO_MALE_COMMAND, 
    TOGGLE_VOICE_GENDER_COMMAND, 
    MEMORY_COMMANDS, 
    FORGET_COMMANDS, 
    MEMORY_SUMMARY_COMMANDS, 
    MEMORY_STATEMENTS, 
    SYMBOLS_REPLACEMENTS, 
    MATH_ANSWER_PREFIXS,
    PRONUNCIATION_MAP
)

from .input_analyzer import (
    normalize_input, 
    remove_wake_word, 
    input_processor, 
    get_local_response, 
    extract_strings, 
    command_vocabulary, 
    correct_command_input, 
    is_farewell, 
    is_greeting, 
    get_current_time, 
    get_current_date
)