import streamlit as st
import os
import json
import commentjson

import configuration

def run_algo(file, data):
    # get config values
    lean_location = configuration.get_value("path")
    language = configuration.get_value("language")
    algorithm_location = os.path.join(lean_location, f"Algorithm.{language}")

    # check if the algorithm folder for the laguage exists
    if not os.path.isdir(algorithm_location):
        st.write(f"Can't find the Algorithm.{language} folder. Check your config.")
        return

    # make sure there is a VisalQuant subfolder so we don't overwrite any other algos
    algorithm_location = os.path.join(algorithm_location, "VisualQuant")
    if not os.path.isdir(algorithm_location):
        os.mkdir(algorithm_location)
    
    # copys the algo into the Lean folder
    algorithm_location = os.path.join(algorithm_location, file.name)
    with open(algorithm_location, "wb") as f:
        f.write(data)

    # open the laucher config
    lauch_file = os.path.join(lean_location, "Launcher/config.json")

    if not os.path.isfile(lauch_file):
        st.write("Can't find Launcher/config.json. Check your config.")
        return

    with open(lauch_file, "r") as f:
        lauch_config = commentjson.load(f)

    algo_name = file.name.split(".")[0]

    # change and save the laucher config
    lauch_config["environment"] = configuration.get_value("environment")
    lauch_config["algorithm-type-name"] = algo_name
    lauch_config["algorithm-language"] = language
    lauch_config["algorithm-location"] = f"../../../Algorithm.{language}/VisualQuant/{file.name}"

    with open(lauch_file, "w") as f:
        json.dump(lauch_config, f, indent=4)


    # call the shell script to start the docker container
    # TODO make it cross platform by selecting the right script to run
    os.system(os.path.join(lean_location, "run_docker.sh"))

    log_expander = st.beta_expander("Log")
    with log_expander:
        with open(os.path.join(lean_location, f"Results/{algo_name}-log.txt"), "r") as f:
            st.text(f.read())

    st.text("")
    st.write("DONE!")


def app():
    st.title("Execute")

    st.header("Select an algorithm")
    st.write("choose a file")
    file = st.file_uploader("")

    if file is not None:
        data = file.read()
        expander = st.beta_expander(file.name)
        with expander:
            encoding = configuration.get_value("encoding")
            st.code(data.decode(encoding))

        st.text("")
        st.text("")

        if st.button("RUN"):
            run_algo(file, data)
