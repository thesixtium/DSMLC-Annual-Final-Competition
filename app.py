import streamlit as st
import requests
import random

stock = ""
buy_it = 0

def main():
    global stock
    global buy_it

    error_messages = [
        "Something went wrong... have you tried killing processes, score, or sacrifice children?",
        "There's an error, are all your versions and flavors right? Consult Gordon Ramsay?",
        "Bro how did you get this error message? GL HF",
        "Keyboard not found. Press a button on the non-existent keyboard to fix it.",
        "Something happened, but I'm not telling you what.",
        "An error occurred while displaying the previous error.",
        "Error displaying the error message you're looking at right now.",
        "Operation completed, but that doesn’t mean it’s error free.",
        "You haven't had an error message in at least one click, so here's one to let you know I care <3"
    ]

    st.title("Happy Stocks")
    st.info(
        "Buying stocks off of happiness, not math (Much like how I do my STAT tests)"
    )

    with st.form("my_form"):
        prompt = st.text_input(
            "Stock: (Leave Blank for Random)",
            max_chars=5,
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            url = ""
            if prompt == "":
                url = "http://localhost:8000/rstock"
            else:
                url = "http://localhost:8000/stock"

            with st.spinner("Crunching (real) numbers..."):
                try:
                    response = requests.get(
                        url=url,
                        params={
                            "prompt": prompt
                        },
                        stream=True,
                    )

                    response = response.content.decode("utf-8")[1:-1].split(",")
                    stock = response[0]
                    buy_it = response[1]

                except Exception as e:
                    st.error(str(f"{random.choice(error_messages)}\n\n{e}"))

                finally:
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        st.metric("Last Stock Selected", stock)
                    with col2:
                        st.metric("How Happy It'll Make You", str(f"{round(float(buy_it) * 100, 2)} %"))
                    with col3:
                        verdicts = [
                            # Bad, is under 0.1
                            [
                                "Buy if you want to be sad",
                                "My 8-ball says no",
                                "Yeaaaaaaaaaaah... no",
                                "F triple minus",
                                "So bad I'm tempted to give an error message"
                            ],

                            # Kinda bad, under 0.2
                            [
                                "I wouldn't buy it, but you do you",
                                "Probably not (but it might be a fun story)",
                                "Mom said no"
                            ],

                            # Neutral, under 0.3
                            [
                                "I feel as strongly about this as I do about Microsoft Access",
                                "Kinda like my elementary school teacher: bland",
                                "About as exciting as plane rice",
                                "As scary as my girlfriend (she's not scary)"
                            ],

                            # Kinda Good, under 0.5
                            [
                                "Better than my last ex for sure",
                                "Yeah, why not?"
                            ],

                            # Good, else
                            [
                                "I'd marry it if it was a person",
                                "Almost as good as AJR"
                            ]
                        ]

                        if float(buy_it) < 0.1:
                            st.metric("Really Bad")
                            st.markdown(f"{random.choice(verdicts[0])}")
                        elif float(buy_it) < 0.2:
                            st.subheader("Bad")
                            st.markdown(f"{random.choice(verdicts[1])}")
                        elif float(buy_it) < 0.3:
                            st.subheader("Neutral")
                            st.markdown(f"{random.choice(verdicts[2])}")
                        elif float(buy_it) < 0.5:
                            st.subheader("Good")
                            st.markdown(f"{random.choice(verdicts[3])}")
                        else:
                            st.subheader("Really Good")
                            st.markdown(f"{random.choice(verdicts[4])}")

if __name__ == "__main__":
    main()
