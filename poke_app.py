import streamlit as st
from Pokémon_Explorer import main, compare_pokemon


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Pokémon Explorer",
    page_icon="⚡",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("⚡ Pokémon Explorer")
st.write("Search for a Pokémon or compare two Pokémon.")


# =========================================================
# TABS
# =========================================================

search_tab, compare_tab = st.tabs(
    ["🔎 Search Pokémon", "⚔️ Compare Pokémon"]
)


# =========================================================
# SEARCH POKÉMON
# =========================================================

with search_tab:

    st.header("🔎 Search Pokémon")

    name = st.text_input(
        "Enter Pokémon name",
        placeholder="Example: Pikachu"
    )

    if st.button("🔍 Search Pokémon", type="primary"):

        if name.strip() == "":
            st.warning("Please enter a Pokémon name.")

        else:

            with st.spinner("Loading Pokémon..."):

                pokemon = main(name)

            if "error" in pokemon:

                st.error(pokemon["error"])

            else:

                st.divider()

                # Pokémon name
                st.header(
                    f"⚡ {pokemon['name'].capitalize()}"
                )

                # -----------------------------------------
                # IMAGE
                # -----------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    if pokemon["image"]:
                        st.image(
                            pokemon["image"],
                            width=300
                        )

                # -----------------------------------------
                # BASIC INFORMATION
                # -----------------------------------------

                with col2:

                    st.subheader("📋 Information")

                    st.write(
                        f"**Name:** "
                        f"{pokemon['name'].capitalize()}"
                    )

                    st.write(
                        f"**Height:** "
                        f"{pokemon['height']} m"
                    )

                    st.write(
                        f"**Weight:** "
                        f"{pokemon['weight']} kg"
                    )

                    st.write(
                        "**Types:** "
                        + ", ".join(
                            t.capitalize()
                            for t in pokemon["types"]
                        )
                    )

                    st.write("**Abilities:**")

                    for ability in pokemon["abilities"]:
                        st.write(
                            f"- {ability.capitalize()}"
                        )

                # -----------------------------------------
                # STATS
                # -----------------------------------------

                st.divider()

                st.subheader("📊 Base Stats")

                for stat, value in pokemon["stats"].items():

                    stat_name = (
                        stat
                        .replace("-", " ")
                        .title()
                    )

                    st.write(
                        f"**{stat_name}: {value}**"
                    )

                    st.progress(
                        min(value / 255, 1.0)
                    )


# =========================================================
# COMPARE POKÉMON
# =========================================================

with compare_tab:

    st.header("⚔️ Compare Pokémon")

    st.write(
        "Enter two Pokémon names and compare their "
        "base stats."
    )

    # -----------------------------------------
    # INPUTS
    # -----------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        pokemon1_name = st.text_input(
            "🥊 First Pokémon",
            placeholder="Example: Pikachu",
            key="pokemon_one"
        )

    with col2:

        pokemon2_name = st.text_input(
            "🥊 Second Pokémon",
            placeholder="Example: Charizard",
            key="pokemon_two"
        )

    st.write("")

    # -----------------------------------------
    # COMPARE BUTTON
    # -----------------------------------------

    compare_button = st.button(
        "⚔️ COMPARE POKÉMON",
        type="primary",
        use_container_width=True
    )

    # -----------------------------------------
    # RUN COMPARISON
    # -----------------------------------------

    if compare_button:

        if (
            pokemon1_name.strip() == ""
            or pokemon2_name.strip() == ""
        ):

            st.warning(
                "Please enter both Pokémon names."
            )

        else:

            with st.spinner("Comparing Pokémon..."):

                try:

                    result = compare_pokemon(
                        pokemon1_name,
                        pokemon2_name
                    )

                except Exception as error:

                    st.error(
                        f"Could not compare Pokémon: {error}"
                    )

                    st.stop()

            # -----------------------------------------
            # GET POKÉMON DATA
            # -----------------------------------------

            pokemon1 = result["pokemon1"]
            pokemon2 = result["pokemon2"]

            # -----------------------------------------
            # DISPLAY POKÉMON
            # -----------------------------------------

            st.divider()

            col1, col2 = st.columns(2)

            # =========================================
            # POKÉMON 1
            # =========================================

            with col1:

                st.subheader(
                    f"⚡ {pokemon1['name'].capitalize()}"
                )

                if pokemon1["image"]:

                    st.image(
                        pokemon1["image"],
                        width=250
                    )

                st.write(
                    f"**Height:** "
                    f"{pokemon1['height']} m"
                )

                st.write(
                    f"**Weight:** "
                    f"{pokemon1['weight']} kg"
                )

                st.write(
                    "**Types:** "
                    + ", ".join(
                        t.capitalize()
                        for t in pokemon1["types"]
                    )
                )

                st.write("**Abilities:**")

                for ability in pokemon1["abilities"]:

                    st.write(
                        f"- {ability.capitalize()}"
                    )

            # =========================================
            # POKÉMON 2
            # =========================================

            with col2:

                st.subheader(
                    f"🔥 {pokemon2['name'].capitalize()}"
                )

                if pokemon2["image"]:

                    st.image(
                        pokemon2["image"],
                        width=250
                    )

                st.write(
                    f"**Height:** "
                    f"{pokemon2['height']} m"
                )

                st.write(
                    f"**Weight:** "
                    f"{pokemon2['weight']} kg"
                )

                st.write(
                    "**Types:** "
                    + ", ".join(
                        t.capitalize()
                        for t in pokemon2["types"]
                    )
                )

                st.write("**Abilities:**")

                for ability in pokemon2["abilities"]:

                    st.write(
                        f"- {ability.capitalize()}"
                    )

            # -----------------------------------------
            # STAT COMPARISON
            # -----------------------------------------

            st.divider()

            st.subheader("📊 Stat Comparison")

            stats1 = pokemon1["stats"]
            stats2 = pokemon2["stats"]

            for stat in stats1:

                value1 = stats1[stat]
                value2 = stats2[stat]

                stat_name = (
                    stat
                    .replace("-", " ")
                    .title()
                )

                st.markdown(
                    f"### {stat_name}"
                )

                col1, col2 = st.columns(2)

                # Pokémon 1
                with col1:

                    st.write(
                        f"**{pokemon1['name'].capitalize()}**"
                    )

                    st.progress(
                        min(value1 / 255, 1.0)
                    )

                    st.write(
                        f"Score: **{value1}**"
                    )

                # Pokémon 2
                with col2:

                    st.write(
                        f"**{pokemon2['name'].capitalize()}**"
                    )

                    st.progress(
                        min(value2 / 255, 1.0)
                    )

                    st.write(
                        f"Score: **{value2}**"
                    )

                # -------------------------------------
                # WINNER
                # -------------------------------------

                if value1 > value2:

                    st.success(
                        f"🏆 "
                        f"{pokemon1['name'].capitalize()} "
                        f"wins {stat_name}!"
                    )

                elif value2 > value1:

                    st.success(
                        f"🏆 "
                        f"{pokemon2['name'].capitalize()} "
                        f"wins {stat_name}!"
                    )

                else:

                    st.info(
                        f"🤝 Both Pokémon have the same "
                        f"{stat_name}."
                    )

            # -----------------------------------------
            # TOTAL STATS
            # -----------------------------------------

            st.divider()

            st.subheader("🏆 Total Base Stats")

            total1 = sum(
                pokemon1["stats"].values()
            )

            total2 = sum(
                pokemon2["stats"].values()
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    pokemon1["name"].capitalize(),
                    total1
                )

            with col2:

                st.metric(
                    pokemon2["name"].capitalize(),
                    total2
                )

            if total1 > total2:

                st.success(
                    f"🏆 {pokemon1['name'].capitalize()} "
                    f"has higher total base stats!"
                )

            elif total2 > total1:

                st.success(
                    f"🏆 {pokemon2['name'].capitalize()} "
                    f"has higher total base stats!"
                )

            else:

                st.info(
                    "🤝 Both Pokémon have the same "
                    "total base stats!"
                )