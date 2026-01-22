# homePotato
An alexia-like system for the le Potato board.

As of right now, this is a work in progress.
My goal is to replace my Alexia Show with this project.
I want as little external dependencies as possible and it to be as simple as possible, but I know that's a bit much for now.

I currently have a le Potato board, a 5-inch touchscreen, standard USB speakers, and a conference microphone.

Current TODO List:

[ ] Features
    [ ] Normalize volume
        After not interacting with it for 30 min change volume to a default volume so it's not really loud or quiet on first interaction

[ ] Threads
    [ ] Speperate thread for weather/cache
    [ ] Thread for timers
    [ ] Thread for music

[ ] Voice interaction
    [x] Basic voice interaction
        [x] Keyword detection
        [x] Instruction sending
    [ ] Simplify script to minimum necessary (run.py)
    [x] Time of day
    [ ] Weather
    [ ] Spotify ("Full functionality of Spotify")
    [ ] YouTube ("Play a video", NOT big priority)
    [ ] Timer
    [ ] Alarm
    [ ] Search (General Questions)
    [ ] Configuration (Volume, Brightness, Voice, etc.)
    [ ] Voice Options (Volume, Speed, Speaker_ID, etc.)
        [ ] Prefered Voices Script (interact with the prefered voices list from voice alone)
[ ] Screen
    [ ] Widget System (Currently thinking something like quickshell or maybe a godot application)
        [ ] Clock
        [ ] Weather
        [ ] Spotify
        [ ] YouTube
        [ ] Timer
        [ ] Alarm
        [ ] Search
        [ ] Configuration
    [ ] I'm sure something else but can't think of it right now
[ ] Scripts
    [ ] Start from zero
        [ ] Flash os to microSD (ideally a minimal OS)
        [ ] Install Software
        [ ] Auto-start homePotato
        [ ] From git clone able to get FULL functioning of homePotato
    [ ] Downloads
        [ ] Vosk Models
        [ ] Piper Voices
        [ ] Custom Images (Wallpapers, icons, etc.)
    [x] Python Environment
    [ ] Prefered Voices
        [ ] Bash script to determine which voices are preferred
            [ ] Play each voice and have user input (yes/no/pass)
            [ ] Be able to return to script later and modify
            [ ] Be able to have multiple lists
            [ ] Random voice option will pick a number from the prefered list if it exists
