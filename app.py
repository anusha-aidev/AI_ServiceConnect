import streamlit as st

from database import (
    get_services,
    get_providers,
    create_service_request
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI ServiceConnect",
    page_icon="🤝",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤝 AI ServiceConnect")

st.subheader(
    "An Intelligent AI-Powered Human Service Marketplace"
)

st.write(
    """
    AI ServiceConnect helps customers find suitable, trusted,
    and available human service providers using AI-powered
    service understanding and provider matching.
    """
)

st.divider()


# ============================================================
# DATABASE CONNECTION
# ============================================================

try:

    services = get_services()

    providers = get_providers()

except Exception as e:

    st.error("❌ Unable to connect to MySQL database.")

    st.error(str(e))

    st.info(
        """
        Please check:

        1. MySQL80 service is running
        2. Your .env file exists
        3. DB_PASSWORD is correct
        4. Database name is ai_serviceconnect
        """
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🤝 AI ServiceConnect")

    st.write(
        """
        **Our goal**

        Connect customers with the right human
        service provider quickly and safely.
        """
    )

    st.divider()

    st.subheader("📊 Platform")

    st.metric(
        "Available Services",
        len(services)
    )

    st.metric(
        "Registered Providers",
        len(providers)
    )

    st.divider()

    st.caption(
        "AI ServiceConnect MVP"
    )


# ============================================================
# CUSTOMER REQUEST SECTION
# ============================================================

st.header("🔎 Find a Service Provider")

st.write(
    """
    Describe your problem in normal language.
    Our system will use your service type, location,
    urgency, provider availability, rating and experience
    to recommend suitable providers.
    """
)


# ------------------------------------------------------------
# Customer request
# ------------------------------------------------------------

request_text = st.text_area(

    "📝 Describe your service requirement",

    placeholder=(
        "Example: My AC is not cooling properly. "
        "I need an AC technician in Hyderabad today."
    ),

    height=120
)


# ------------------------------------------------------------
# Location
# ------------------------------------------------------------

location = st.text_input(

    "📍 Your Location",

    placeholder="Example: Hyderabad"
)


# ------------------------------------------------------------
# Urgency
# ------------------------------------------------------------

urgency = st.selectbox(

    "⏰ When do you need the service?",

    [
        "Today",
        "Tomorrow",
        "Within 3 days",
        "Within a week",
        "Not urgent"
    ]
)


# ============================================================
# SERVICE SELECTION
# ============================================================

if not services:

    st.warning(
        "⚠️ No services are available in the database."
    )

    st.stop()


service_names = [

    service["service_name"]

    for service in services

]


selected_service = st.selectbox(

    "🛠️ Select the Service",

    service_names
)


# ============================================================
# FIND PROVIDERS BUTTON
# ============================================================

if st.button(
    "🔍 Find Best Providers",
    type="primary"
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not request_text.strip():

        st.warning(
            "⚠️ Please describe your service requirement."
        )

        st.stop()


    if not location.strip():

        st.warning(
            "⚠️ Please enter your location."
        )

        st.stop()


    # --------------------------------------------------------
    # FIND SELECTED SERVICE
    # --------------------------------------------------------

    selected_service_data = next(

        (
            service
            for service in services

            if service["service_name"]
            == selected_service
        ),

        None

    )


    if selected_service_data is None:

        st.error(
            "❌ Selected service was not found."
        )

        st.stop()


    service_id = selected_service_data["service_id"]


    # ========================================================
    # SAVE CUSTOMER REQUEST
    # ========================================================

    try:

        request_id = create_service_request(

            user_id=1,

            service_id=service_id,

            request_text=request_text,

            problem_description=request_text,

            location=location,

            urgency=urgency

        )

        st.success(
            f"✅ Service request created successfully! "
            f"Request ID: {request_id}"
        )

    except Exception as e:

        st.error(
            "❌ Failed to save service request."
        )

        st.error(str(e))

        st.stop()


    # ========================================================
    # PROVIDER MATCHING
    # ========================================================

    




    # ========================================================
    # CALCULATE MATCH SCORE
    # ========================================================

    for provider in providers:


        # ----------------------------------------------------
        # SERVICE MATCH
        # ----------------------------------------------------

        service_match = (

            provider["service_type"].strip().lower()

            == selected_service.strip().lower()

        )


        # ----------------------------------------------------
        # LOCATION MATCH
        # ----------------------------------------------------

        provider_location = (

            provider["location"] or ""

        ).strip().lower()


        customer_location = (

            location or ""

        ).strip().lower()


        location_match = (

            customer_location
            in provider_location

        )


        # ----------------------------------------------------
        # AVAILABILITY
        # ----------------------------------------------------

        availability = (

            provider["availability"] or ""

        ).strip().lower()


        is_available = (

            availability == "available"

        )


        # ----------------------------------------------------
        # ONLY MATCH CORRECT SERVICE + AVAILABLE PROVIDERS
        # ----------------------------------------------------

        if service_match and is_available:


            # =================================================
            # MATCHING SCORE
            # =================================================

            score = 0


            # Rating
            rating = float(

                provider["rating"] or 0

            )

            score += rating * 20


            # Experience
            experience = int(

                provider["experience_years"] or 0

            )

            score += min(
                experience * 2,
                20
            )


            # Location
            if location_match:

                score += 20


            # Verified provider
            if provider["verified"]:

                score += 10


            # ------------------------------------------------
            # Store score
            # ------------------------------------------------

            provider_copy = provider.copy()

            provider_copy["match_score"] = round(
                score,
                2
            )

            provider_copy["location_match"] = (
                location_match
            )

            matching_providers.append(
                provider_copy
            )


    # ========================================================
    # SORT PROVIDERS
    # ========================================================

    matching_providers.sort(

        key=lambda provider:
        provider["match_score"],

        reverse=True

    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    st.divider()

    st.header(
        "⭐ Recommended Service Providers"
    )


    if not matching_providers:

        st.warning(
            """
            No suitable providers were found.

            Try:
            • Selecting another service
            • Entering another location
            • Checking again later
            """
        )


    else:

        st.success(

            f"🎯 Found {len(matching_providers)} "
            f"matching provider(s)."

        )


        # ====================================================
        # PROVIDER CARDS
        # ====================================================

        for rank, provider in enumerate(
            matching_providers,
            start=1
        ):


            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [3, 1]
                )


                # ============================================
                # PROVIDER INFORMATION
                # ============================================

                with col1:

                    st.subheader(

                        f"#{rank} 👨‍🔧 "
                        f"{provider['name']}"

                    )


                    st.write(

                        f"🛠️ **Service:** "
                        f"{provider['service_type']}"

                    )


                    st.write(

                        f"⭐ **Rating:** "
                        f"{provider['rating']} / 5"

                    )


                    st.write(

                        f"💼 **Experience:** "
                        f"{provider['experience_years']} years"

                    )


                    st.write(

                        f"📍 **Location:** "
                        f"{provider['location']}"

                    )


                    st.write(

                        f"💰 **Price:** "
                        f"₹{provider['price_per_hour']} / hour"

                    )


                    st.write(

                        f"🟢 **Availability:** "
                        f"{provider['availability']}"

                    )


                    if provider["verified"]:

                        st.success(
                            "✓ Verified Provider"
                        )

                    else:

                        st.warning(
                            "⚠ Not Verified"
                        )


                    if provider["location_match"]:

                        st.info(
                            "📍 Location matched"
                        )


                # ============================================
                # MATCH SCORE
                # ============================================

                with col2:

                    st.metric(

                        "Match Score",

                        f"{provider['match_score']}/150"

                    )


                    st.write(
                        "Higher score = better match"
                    )


                    # ========================================
                    # BOOK BUTTON
                    # ========================================

                    if st.button(

                        "📅 Book Now",

                        key=(
                            f"book_"
                            f"{provider['provider_id']}"
                        )

                    ):

                        st.success(

                            f"✅ Booking request sent "
                            f"to {provider['name']}!"

                        )


# ============================================================
# AVAILABLE SERVICES
# ============================================================

st.divider()

st.header(
    "🛠️ Available Services"
)


service_columns = st.columns(3)


for index, service in enumerate(
    services
):

    with service_columns[
        index % 3
    ]:

        st.info(

            f"""
            **{service['service_name']}**

            {service['description']}

            💰 Starting from
            ₹{service['base_price']}
            """

        )


# ============================================================
# HOW THE SYSTEM WORKS
# ============================================================

