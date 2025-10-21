def format_profile_data(profile: dict) -> str:
    """Format user profile for Telegram message in a user-friendly way"""
    
    partners = profile.get("partners", [])
    partners_text = ", ".join([p.get("username", "N/A") for p in partners]) or "None"

    msg = "\n".join([
        f"👤 Username: {profile.get('username', '')}",
        f"📧 Email: {profile.get('email', '')}",
        f"📝 First Name: {profile.get('first_name', '-')}",
        f"📝 Last Name: {profile.get('last_name', '-')}",
        f"🔄 Cycle Length: {profile.get('cycle_length', '-') } days",
        f"📅 Period Duration: {profile.get('period_duration', '-') } days",
        f"🧑‍🤝‍🧑 Partners: {partners_text}",
        f"⚧ Sex: {profile.get('sex', '-')}"
    ])
    
    return msg


def format_user_profile(profile: dict) -> str:
    """
    Convert the API response to a user-friendly string
    """
    lines = [
        f"👤 Username: {profile.get('username', '')}",
        f"📧 Email: {profile.get('email', '')}",
        f"📝 First Name: {profile.get('first_name', '')}",
        f"📝 Last Name: {profile.get('last_name', '')}",
        f"🔄 Cycle Length: {profile.get('cycle_length', '')} days",
        f"📅 Period Duration: {profile.get('period_duration', '')} days",
        f"🧑‍🤝‍🧑 Partners: {', '.join([p['username'] for p in profile.get('partners', [])]) or 'None'}",
        f"⚧ Sex: {profile.get('sex', '')}"
    ]
    return "\n".join(lines)


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
    if period.get("predicted_end_date"):
        formatted += f"• Predict End: {period['predicted_end_date']}\n"
    if period.get("cycle_length"):
        formatted += f"• Cycle: {period['cycle_length']} days\n"
    if period.get("period_duration"):
        formatted += f"• Duration: {period['period_duration']} days\n"
    if period.get("symptoms"):
        formatted += f"• Symptoms: {period['symptoms']}\n"
    if period.get("medication"):
        formatted += f"• Medication: {period['medication']}\n"
    if period.get("next_period_start_date"):
        formatted += f"• Next Period: {period['next_period_start_date']}\n"

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
    Handles both 'self' and 'partner_tracking' view types
    """
    data = analysis.get("data", {})
    view_type = analysis.get("view_type", "self")
    
    # Partner tracking view (for male users tracking their partner)
    if view_type == "partner_tracking":
        tracking_mode = data.get("tracking_mode", "")
        partner_info = data.get("partner_info", {})
        support_tips = data.get("support_tips", [])
        
        message = f"*💑 Partner Cycle Tracking*\n\n"
        
        if partner_info:
            partner_name = partner_info.get("name", "Your Partner")
            message += f"*Partner:* {partner_name}\n"
            
            next_period = partner_info.get("next_period_date", "N/A")
            days_until = partner_info.get("days_until_period", "N/A")
            message += f"*Next Period:* {next_period}\n"
            message += f"*Days Until Period:* {days_until} days\n"
            
            current_phase = partner_info.get("current_phase", "N/A")
            message += f"*Current Phase:* {current_phase}\n"
            
            is_on_period = partner_info.get("is_on_period", False)
            message += f"*Period Status:* {'🔴 On Period' if is_on_period else '⚪ Not on Period'}\n"
            
            regularity = partner_info.get("cycle_regularity", "N/A")
            message += f"*Cycle Regularity:* {regularity}%\n"
            
            avg_cycle = partner_info.get("average_cycle_length", "N/A")
            message += f"*Average Cycle:* {avg_cycle} days\n"
        
        if support_tips:
            message += f"\n*💡 Support Tips:*\n"
            for tip in support_tips:
                message += f"• {tip}\n"
        
        return message
    
    # Self view (for female users or male users viewing their own data)
    gender = data.get("gender", "female")
    
    # Basic cycle statistics
    average_cycle = data.get("average_cycle", "N/A")
    regularity_score = data.get("regularity_score", "N/A")
    cycle_variations = data.get("cycle_variations", [])
    prediction_reliability = data.get("prediction_reliability", "N/A")
    next_predicted_date = data.get("next_predicted_date", "N/A")
    
    variations_text = ", ".join(str(v) for v in cycle_variations) if cycle_variations else "N/A"
    
    message = f"*📊 Cycle Analysis*\n\n"
    message += f"*Average Cycle Length:* {average_cycle} days\n"
    message += f"*Regularity Score:* {regularity_score}%\n"
    message += f"*Cycle Variations:* {variations_text}\n"
    message += f"*Prediction Reliability:* {prediction_reliability}%\n"
    message += f"*Next Predicted Period:* {next_predicted_date}\n"
    
    # Current status section
    current_status = data.get("current_status", {})
    if current_status:
        message += f"\n*📍 Current Status*\n\n"
        
        if gender == "male":
            # Male user - simplified status
            phase = current_status.get("phase", "N/A")
            phase_description = current_status.get("phase_description", "")
            message += f"*Phase:* {phase}\n"
            if phase_description:
                message += f"*Note:* {phase_description}\n"
        else:
            # Female user - detailed status
            is_on_period = current_status.get("is_on_period", False)
            phase = current_status.get("phase", "N/A")
            phase_description = current_status.get("phase_description", "")
            
            if is_on_period:
                current_day = current_status.get("current_day_of_period", "N/A")
                message += f"🔴 *On Period* - Day {current_day}\n"
            else:
                message += f"⚪ *Not on Period*\n"
            
            cycle_day = current_status.get("cycle_day")
            if cycle_day:
                message += f"*Cycle Day:* {cycle_day}\n"
            
            message += f"*Phase:* {phase}\n"
            
            if phase_description:
                message += f"*Description:* {phase_description}\n"
            
            days_until_next = current_status.get("days_until_next_period")
            if days_until_next is not None:
                message += f"*Days Until Next Period:* {days_until_next}\n"
            
            is_fertile = current_status.get("is_fertile_window", False)
            message += f"*Fertile Window:* {'Yes 🌸' if is_fertile else 'No'}\n"
    
    return message


def format_notification_list(notifications: list, count: int, unread_only: bool = False) -> str:
    """Format notification list for display"""
    if not notifications:
        return "📭 No notifications."
    
    title = "🔔 *Unread Notifications*" if unread_only else "🔔 *All Notifications*"
    message = f"{title}\n\n"
    message += f"Total: {count}\n\n"
    
    # Emoji mapping
    emoji_map = {
        "PERIOD_COMING": "🔴",
        "PERIOD_STARTED": "🩸",
        "PERIOD_LATE": "⚠️",
        "OVULATION_COMING": "🌸",
        "FERTILE_WINDOW": "💐",
        "PMS_PHASE": "😔",
        "SYMPTOM_REMINDER": "📝",
        "WELLNESS_REMINDER": "💪",
        "PARTNER_PERIOD": "💑",
        "PARTNER_PMS": "🤝"
    }
    
    for i, notif in enumerate(notifications[:10], 1):  # Show max 10
        notif_type = notif.get("notification_type", "")
        title = notif.get("title", "Notification")
        msg = notif.get("message", "")
        is_read = notif.get("is_read", False)
        
        emoji = emoji_map.get(notif_type, "🔔")
        read_status = "✅" if is_read else "🆕"
        
        message += f"{i}. {emoji} {read_status} *{title}*\n"
        message += f"   {msg[:80]}{'...' if len(msg) > 80 else ''}\n\n"
    
    if count > 10:
        message += f"\n... and {count - 10} more notifications"
    
    return message


def format_notification_preferences(preferences: dict) -> str:
    """Format notification preferences for display"""
    message = "⚙️ *Notification Settings*\n\n"
    
    # Period notifications
    message += "*Period Notifications:*\n"
    message += f"• Period Coming: {'✅' if preferences.get('period_started_alert') else '❌'}\n"
    message += f"• Period Late: {'✅' if preferences.get('period_late_alert') else '❌'}\n"
    message += f"• Reminder Days: {preferences.get('period_reminder_days', 3)} days before\n\n"
    
    # Cycle notifications
    message += "*Cycle Notifications:*\n"
    message += f"• Ovulation: {'✅' if preferences.get('ovulation_alert') else '❌'}\n"
    message += f"• Fertile Window: {'✅' if preferences.get('fertile_window_alert') else '❌'}\n"
    message += f"• PMS Phase: {'✅' if preferences.get('pms_phase_alert') else '❌'}\n\n"
    
    # Reminders
    message += "*Reminders:*\n"
    message += f"• Symptom Logging: {'✅' if preferences.get('symptom_reminder') else '❌'}\n"
    message += f"• Wellness Check-in: {'✅' if preferences.get('wellness_reminder') else '❌'}\n\n"
    
    # Partner notifications
    message += "*Partner Notifications:*\n"
    message += f"• Partner's Period: {'✅' if preferences.get('partner_period_alert') else '❌'}\n"
    message += f"• Partner's PMS: {'✅' if preferences.get('partner_pms_alert') else '❌'}\n\n"
    
    # Timing
    preferred_time = preferences.get('preferred_notification_time', '09:00:00')
    message += f"*Preferred Time:* {preferred_time}\n"
    
    return message
