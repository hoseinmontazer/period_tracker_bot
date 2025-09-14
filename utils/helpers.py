def format_profile_data(profile: dict) -> str:
    """Format user profile for Telegram message"""
    user = profile.get("user", {})
    username = user.get("username", "N/A")
    email = user.get("email", "N/A")
    sex = user.get("sex", "N/A").capitalize()

    first_name = profile.get("first_name") or "-"
    last_name = profile.get("last_name") or "-"
    cycle_length = profile.get("cycle_length", "N/A")
    period_duration = profile.get("period_duration", "N/A")

    partners = profile.get("partners", [])
    if partners:
        partners_text = "\n".join(
            [f"👥 {p.get('username', 'N/A')} ({p.get('email', '-')})" for p in partners]
        )
    else:
        partners_text = "No partners connected."

    msg = (
        f"*👤 Profile Information*\n\n"
        f"*Username:* {username}\n"
        f"*Email:* {email}\n"
        f"*Sex:* {sex}\n"
        f"*First Name:* {first_name}\n"
        f"*Last Name:* {last_name}\n"
        f"*Cycle Length:* {cycle_length} days\n"
        f"*Period Duration:* {period_duration} days\n\n"
        f"*Partners:*\n{partners_text}"
    )
    return msg

    return formatted

def format_period_data(periods_data):
    """Format period data for display"""
    if not periods_data or not isinstance(periods_data, list):
        return "No period data available."
    
    if len(periods_data) == 0:
        return "No periods tracked yet."
    
    formatted = "📅 *Period History:*\n\n"
    
    for i, period in enumerate(periods_data[:5]):  # Show only last 5 periods
        formatted += f"*Period {i+1}:*\n"
        formatted += format_single_period(period)
        formatted += "\n"
    
    if len(periods_data) > 5:
        formatted += f"\n... and {len(periods_data) - 5} more periods"
    
    return formatted

def format_single_period(period):
    """Format single period entry"""
    formatted = ""
    if period.get("start_date"):
        formatted += f"• Start: {period['start_date']}\n"
    if period.get("end_date"):
        formatted += f"• End: {period['end_date']}\n"
    if period.get("cycle_length"):
        formatted += f"• Cycle: {period['cycle_length']} days\n"
    if period.get("period_duration"):
        formatted += f"• Duration: {period['period_duration']} days\n"
    if period.get("symptoms"):
        formatted += f"• Symptoms: {period['symptoms']}\n"
    if period.get("medication"):
        formatted += f"• Medication: {period['medication']}\n"
    return formatted

# def format_analysis_data(analysis_data):
#     """Format cycle analysis data for display"""
#     if not analysis_data:
#         return "No analysis data available."
    
#     formatted = "📊 *Cycle Analysis:*\n\n"
    
#     if analysis_data.get("average_cycle"):
#         formatted += f"• *Average Cycle:* {analysis_data['average_cycle']} days\n"
    
#     if analysis_data.get("average_period_duration"):
#         formatted += f"• *Average Period:* {analysis_data['average_period_duration']} days\n"
    
#     if analysis_data.get("cycle_regularity"):
#         formatted += f"• *Regularity:* {analysis_data['cycle_regularity']}\n"
    
#     if analysis_data.get("next_period_prediction"):
#         formatted += f"• *Next Period Prediction:* {analysis_data['next_period_prediction']}\n"
    
#     if analysis_data.get("fertile_window_start") and analysis_data.get("fertile_window_end"):
#         formatted += f"• *Fertile Window:* {analysis_data['fertile_window_start']} to {analysis_data['fertile_window_end']}\n"
    
#     if analysis_data.get("ovulation_prediction"):
#         formatted += f"• *Ovulation Prediction:* {analysis_data['ovulation_prediction']}\n"
    
#     if analysis_data.get("common_symptoms"):
#         symptoms = analysis_data['common_symptoms']
#         if symptoms:
#             formatted += f"• *Common Symptoms:* {', '.join(symptoms)}\n"
    
#     return formatted


def format_analysis_data(analysis: dict) -> str:
    """
    Format the cycle analysis data for Telegram Markdown message
    """
    data = analysis.get("data", {})
    average_cycle = data.get("average_cycle", "N/A")
    regularity_score = data.get("regularity_score", "N/A")
    cycle_variations = data.get("cycle_variations", [])
    prediction_reliability = data.get("prediction_reliability", "N/A")
    next_predicted_date = data.get("next_predicted_date", "N/A")

    variations_text = ", ".join(str(v) for v in cycle_variations) if cycle_variations else "N/A"

    message = (
        f"*📊 Cycle Analysis*\n\n"
        f"*Average Cycle Length:* {average_cycle} days\n"
        f"*Regularity Score:* {regularity_score}\n"
        f"*Cycle Variations:* {variations_text}\n"
        f"*Prediction Reliability:* {prediction_reliability}/10\n"
        f"*Next Predicted Period:* {next_predicted_date}\n"
    )
    return message
