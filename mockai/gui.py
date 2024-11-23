import json
import time
import uuid

import streamlit as st

from mockai.models import FunctionOutput, PreDeterminedResponse, PreDeterminedResponses


def generate_key():
    return uuid.uuid4().hex


def create_sample_function_output():
    return FunctionOutput(
        name="example_function",
        arguments={"example_key": "example_value"},
    )


def write_responses_to_file(responses: list[PreDeterminedResponse]):
    responses_dict = [m.model_dump() for m in responses]

    content = json.dumps(responses_dict, indent=2, ensure_ascii=False)

    with open(file_path, "w") as f:
        f.write(content)


def open_file(file: str) -> list[PreDeterminedResponse]:
    with open(file, "r") as f:
        return PreDeterminedResponses.validate_json(f.read())


def function_output(output: FunctionOutput | list[FunctionOutput]):
    if isinstance(output, FunctionOutput):
        output = [output]

    st.text("Output")

    st.button(
        "Add function",
        on_click=output.append(create_sample_function_output()),
        key=generate_key(),
    )

    for o in output:
        with st.expander(o.name):
            o.name = st.text_input("name", o.name, key=generate_key())

            clone = o.arguments.copy()
            for k, v in clone.items():
                col1, col2 = st.columns(2)

                with col1:
                    new_key = st.text_input("key", k, key=generate_key())

                with col2:
                    new_value = st.text_input("value", v, key=generate_key())

                o.arguments[k] = new_value
                o.arguments[new_key] = o.arguments.pop(k)

            st.button("Add field", key=generate_key())

    return output


def form_component(n, r_type, input, output):
    with st.container(border=False):
        input = st.text_input("Input", input, key=generate_key())

        if r_type == "text":
            output = st.text_input("Output", output, key=generate_key())
        else:
            try:
                output = function_output(output)
            except AttributeError:
                output = function_output(create_sample_function_output())

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update", key=generate_key()):
                responses[n].input = input
                responses[n].output = output

                write_responses_to_file(responses)

                success = st.success("Response updated!", icon="✅")
                time.sleep(3)
                success.empty()

        with col2:
            if st.button("Delete", key=generate_key()):
                responses.pop(n)

                write_responses_to_file(responses)

                success = st.success("Response deleted!", icon="✅")
                time.sleep(3)
                success.empty()

                st.rerun()


if __name__ == "__main__":
    file_path = "./tests/responses.json"

    responses = open_file(file_path)

    st.set_page_config(page_title="MockAI GUI", page_icon=":wrench:")

    st.title("MockAI Responses")

    for idx, response in enumerate(responses):
        with st.container(border=True):
            st.header(f"Response {idx + 1}", divider=True)

            r_type = st.selectbox(
                "Type",
                ["text", "function"],
                0 if response.type == "text" else 1,
                key=generate_key(),
            )

            form_component(idx, r_type, response.input, response.output)

    new_response = st.button("Add response")

    if new_response:
        responses.append(PreDeterminedResponse(type="text", input="", output=""))

        write_responses_to_file(responses)

        st.rerun()
