from streamlit import bootstrap

real_script = 'streamlit_app.py'

bootstrap.run(real_script, f'run.py {real_script}', [])