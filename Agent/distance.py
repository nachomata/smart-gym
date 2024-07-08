import grovepi
import time
import display

ultrasonic_ranger = 2
bottom_threshold = 25
top_threshold = 20
exercise_end_time = 10

def count_repetitions(user_name):
    display.setRGB(0, 255, 255)
    display.setText(f"{user_name}: 15kg\nRepetitions: 0")
    repetitions = 0
    in_exercise = False
    start_rest_time = None
    
    while True:
        try:
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)
            print(f"Distance: {distance} cm")
            if distance < top_threshold and not in_exercise:
                in_exercise = True
                print("Started repetition")
            
            if distance > bottom_threshold and in_exercise:
                in_exercise = False
                repetitions += 1
                print(f"Completed repetition, count: {repetitions}")
                display.setText(f"{user_name}: 15kg\nRepetitions: {repetitions}")
            
            if distance > bottom_threshold:
                if start_rest_time is None:
                    start_rest_time = time.time()
                elif time.time() - start_rest_time > exercise_end_time:
                    if repetitions > 0:
                        print("Exercise ended. Total repetitions: {}".format(repetitions))
                        return repetitions
            else:
                start_rest_time = None

        except Exception as e:
            print("Error: {}".format(e))
        
        time.sleep(1)


activity_timeout = 120  # 2 minutes

def wait_for_resume_activity():
    start_time = time.time()
    
    while True:
        try:
            distance = grovepi.ultrasonicRead(ultrasonic_ranger)
            print(f"Distance: {distance} cm")
            display.setRGB(255, 255, 0)
            display.setText(f"Taking a break\nLog out in {activity_timeout - int(time.time() - start_time)}")
            if distance < bottom_threshold:
                print("Machine in use detected.")
                return True
            
            if time.time() - start_time > activity_timeout:
                print(f"No activity detected for {activity_timeout} seconds.")
                display.setRGB(255, 0, 0)
                display.setText("Logging out")
                time.sleep(2)
                return False
        
        except Exception as e:
            print("Error: {}".format(e))
        
        time.sleep(1)

if __name__ == '__main__':
    repetitions = count_repetitions("nacho")
    print("Total repetitions: {}".format(repetitions))