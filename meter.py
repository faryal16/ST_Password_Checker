import streamlit as st
import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def classify_password(password):
    score = 0
    criteria = []
    
    if len(password) >= 8:
        score += 20
        criteria.append("✅ Length (8+ chars, 12+ recommended)")
    else:
        criteria.append("❌ Length too short (8+ chars recommended)")
    
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 20
        criteria.append("✅ Upper & lowercase letters")
    else:
        criteria.append("❌ Include both uppercase and lowercase letters.")
    
    if any(c.isdigit() for c in password):
        score += 15
        criteria.append("✅ Contains numbers")
    else:
        criteria.append("❌ Add numbers for better security.")
    
    if any(c in string.punctuation for c in password):
        score += 15
        criteria.append("✅ Contains special characters")
    else:
        criteria.append("❌ Include special characters like @, #, $ for added security.")
    
    common_patterns = ['123', 'abc', 'password', 'qwerty']
    if not any(pattern in password.lower() for pattern in common_patterns):
        score += 15
        criteria.append("✅ No common patterns")
    else:
        criteria.append("❌ Avoid sequential characters like 'abc', '123', etc.")
    
    common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
    if password.lower() not in common_passwords:
        score += 15
        criteria.append("✅ Not a common password")
    else:
        criteria.append("❌ Avoid commonly used passwords.")
    
    if score >= 80:
        strength = "Strong"
        message = "💪 Your password is strong! Well done. Keep it safe."
    elif score >= 50:
        strength = "Average"
        message = "😐 Your password is average. Consider making it longer and more complex."
    else:
        strength = "Weak"
        message = "😞 Your password is weak! Try adding numbers, symbols, and uppercase letters."
    
    return strength, message, score, criteria

# Streamlit UI
st.header("🔒 Password Generator & Strength Meter")

st.write("Check the strength of your own password or Generate a secure password within a length of 6 to 12 characters.")



# User input for checking password strength
st.subheader("🔍 Check Your Password Strength")
user_password = st.text_input("Enter your password", type="password")

if st.button("Check Strength"):
    if user_password:
        strength, message, score, criteria = classify_password(user_password)
        st.subheader(f"Password Strength: {strength} ({score}/100)")
        for criterion in criteria:
            st.write(criterion)
        st.write(message)
    else:
        st.warning("Please enter a password to check its strength.")


st.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)

# User input for password length
st.subheader("🔑 Generate your new Password ")
password_length = st.slider("Select password length", min_value=6, max_value=12, value=8)

if st.button("Generate Password"):
    password = generate_password(password_length)
    strength, message, score, criteria = classify_password(password)
    
    st.success(f"Generated Password: `{password}`")
    st.subheader(f"Password Strength: {strength} ({score}/100)")
    for criterion in criteria:
        st.write(criterion)
    st.write(message)