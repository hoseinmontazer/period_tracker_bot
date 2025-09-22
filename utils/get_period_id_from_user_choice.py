def get_period_id_from_user_choice(period_list, user_choice_str):
    try:
        print(period_list)
        # Convert the string to an integer
        choice_int = int(user_choice_str)
        # Check if the number is within the valid range (1 to list length)
        if 1 <= choice_int <= len(period_list):
            # The list index is one less than the user's choice
            index = choice_int - 1
            # Retrieve the dictionary from the list
            selected_period = period_list[index]
            # Return the 'id' from the selected dictionary
            return selected_period.get('id')
        else:
            print("Invalid choice. Please select a number from the list.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None