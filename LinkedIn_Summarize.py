import os
import json
import streamlit as st
from dotenv import load_dotenv
from Profile_Extraction import search_local_profiles, get_profile_url, fetch_linkedin_profile
from Summary_Generator import generate_summary

load_dotenv()

path1 = os.getenv("INDIA_PROFILES_PATH")
path2 = os.getenv("US_PROFILES_PATH")

json_files = [path1, path2]

def preprocess_profile_data(profile_data):
    # Initialize an empty list to store extracted information
    extracted_info = []
    
    # Extract the basic info
    full_name = profile_data.get("full_name", "")
    if full_name:
        extracted_info.append(f"Full Name: {full_name}")
    
    first_name = profile_data.get("first_name", "")
    last_name = profile_data.get("last_name", "")
    if first_name and last_name:
        extracted_info.append(f"Name: {first_name} {last_name}")
    
    occupation = profile_data.get("occupation", "")
    if occupation:
        extracted_info.append(f"Occupation: {occupation}")
    
    headline = profile_data.get("headline", "")
    if headline:
        extracted_info.append(f"Headline: {headline}")
    
    summary = profile_data.get("summary", "")
    if summary:
        extracted_info.append(f"Summary: {summary}")
    
    country = profile_data.get("country_full_name", "")
    if country:
        extracted_info.append(f"Country: {country}")
    
    # Extract experiences
    experiences = profile_data.get("experiences", [])
    if experiences:
        extracted_info.append("\nExperiences:")
        for exp in experiences:
            title = exp.get("title", "No Title")
            company = exp.get("company", "No Company")
            description = exp.get("description", "No Description")
            location = exp.get("location", "No Location")
            duration = f"{exp.get('starts_at', {}).get('year', 'N/A')} to {exp.get('ends_at', {}).get('year', 'Present')}"
            extracted_info.append(f"- {title} at {company} ({location}, {duration}): {description}")
    
    # Extract education
    education = profile_data.get("education", [])
    if education:
        extracted_info.append("\nEducation:")
        for edu in education:
            school = edu.get("school", "No School")
            degree = edu.get("degree_name", "No Degree")
            field_of_study = edu.get("field_of_study", "No Field of Study")
            duration = f"{edu.get('starts_at', {}).get('year', 'N/A')} to {edu.get('ends_at', {}).get('year', 'Present')}"
            extracted_info.append(f"- {degree} in {field_of_study} from {school} ({duration})")
    
    # Extract accomplishment courses
    accomplishment_courses = profile_data.get("accomplishment_courses", [])
    if accomplishment_courses:
        extracted_info.append("\nAccomplishment Courses:")
        for course in accomplishment_courses:
            name = course.get("name", "No Name")
            number = course.get("number", "No Number")
            extracted_info.append(f"- {name} (Course Number: {number})")
    
    # Extract certifications
    certifications = profile_data.get("certifications", [])
    if certifications:
        extracted_info.append("\nCertifications:")
        for cert in certifications:
            name = cert.get("name", "No Name")
            authority = cert.get("authority", "No Authority")
            extracted_info.append(f"- {name} by {authority}")
    
    # Extract activities
    activities = profile_data.get("activities", [])
    if activities:
        extracted_info.append("\nActivities:")
        for activity in activities:
            title = activity.get("title", "No Title")
            link = activity.get("link", "No Link")
            extracted_info.append(f"- {title} ({link})")
    
    # Combine all extracted information into a single formatted text
    return "\n".join(extracted_info)


st.title("LinkedIn Profile Summary Generator")

name = st.text_input("Enter the full name of the person:")

if st.button("Generate Summary"):
    if not name:
        st.error("Please enter a name.")
    else:
        # Step 1: Check local JSON files (India and US profiles)
        profile_data = search_local_profiles(name, json_files)

        if profile_data:
            st.write(f"Profile found in local files for {name}")
        else:
            st.write(f"Profile not found locally. Initiating Tavily search for {name}...")
            linkedin_url = get_profile_url(name)

            if linkedin_url:
                st.write(f"LinkedIn URL found: {linkedin_url}")
                profile_data = fetch_linkedin_profile(linkedin_url)
                
                if profile_data:
                    st.write("Profile data fetched successfully from ProxyCurl.")
                else:
                    st.error("Failed to fetch profile data from ProxyCurl.")
                    profile_data = None
            else:
                st.error("No valid LinkedIn profile found.")

        if profile_data:
            # Convert profile data to string
            preprocessed_profile_data = preprocess_profile_data(profile_data)

            # Step 2: Generate the profile summary using the LLM
            st.write("Generating profile summary...")
            summary = generate_summary(preprocessed_profile_data)

            if summary:
                st.subheader("Profile Summary")
                st.write(summary)
            else:
                st.error("Failed to generate profile summary.")

