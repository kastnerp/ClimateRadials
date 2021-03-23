call "C:\Users\pkastner\Anaconda3\Scripts\activate.bat" hobo
kernprof -l radial_test.py
python -m line_profiler radial_test.py.lprof
PAUSE