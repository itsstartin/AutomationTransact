import pyautogui
import time
import keyboard
import os
import random

# === Base directory of the current script ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Button image paths (auto-load from same folder) ===
BUTTON_IMAGES = [
    os.path.join(BASE_DIR, 'transfer_ready.png'),
    os.path.join(BASE_DIR, 'submit.png'),
    os.path.join(BASE_DIR, 'sign.png'),
    os.path.join(BASE_DIR, 'confirm.png'),
    os.path.join(BASE_DIR, 'new_transfer.png')
]

# === Region: blocks 5,6,8,9 of 3x3 grid ===
screen_width, screen_height = pyautogui.size()
block_w = screen_width // 3
block_h = screen_height // 3
region_x = block_w
region_y = block_h
region_w = block_w * 2
region_h = block_h * 2

# === Global stop flag ===
stop_flag = False

def set_stop_flag():
    global stop_flag
    stop_flag = True
    print("🛑 Stop signal received (q pressed). Exiting...")

keyboard.add_hotkey('q', set_stop_flag)

# === Realistic click with hover and randomness ===
def realistic_click(location):
    pyautogui.moveTo(location, duration=random.uniform(0.2, 0.9))
    time.sleep(random.uniform(0.3, 0.9))
    pyautogui.click()
    time.sleep(random.uniform(0.3, 0.9))

# === Locate and click button ===
def find_and_click_button(image_path, confidence=0.7):
    print(f"🔍 Waiting for button: {image_path}")
    while not stop_flag:
        try:
            location = pyautogui.locateCenterOnScreen(
                image_path,
                region=(region_x, region_y, region_w, region_h),
                confidence=confidence
            )
            if location:
                print(f"✅ Found and clicking: {image_path}")
                realistic_click(location)
                time.sleep(random.uniform(1.5, 4.9))  # Add delay after click
                return True
        except Exception as e:
            print(f"⚠️ Error locating image: {e}")
        time.sleep(random.uniform(0.8, 3.5))  # Add randomness to retry loop

    print("🛑 Stopped before finding button.")
    return False

# === Click 'sign' button and wait until 'confirm' appears ===
def click_sign_and_wait_for_confirm(sign_img, confirm_img, confidence=0.99):
    while not stop_flag:
        print("🔁 Clicking 'sign' and waiting for 'confirm' to appear...")
        found_sign = False

        try:
            location = pyautogui.locateCenterOnScreen(
                sign_img,
                region=(region_x, region_y, region_w, region_h),
                confidence=confidence
            )
            if location:
                print("✅ 'Sign' found. Clicking...")
                realistic_click(location)
                time.sleep(random.uniform(1.5, 5.0))
                found_sign = True
        except Exception as e:
            print(f"⚠️ Error locating 'sign': {e}")

        if not found_sign:
            time.sleep(random.uniform(1.0, 3.5))
            continue

        # Check once for 'confirm' after clicking 'sign'
        try:
            confirm_location = pyautogui.locateCenterOnScreen(
                confirm_img,
                region=(region_x, region_y, region_w, region_h),
                confidence=confidence
            )
            if confirm_location:
                print("✅ 'Confirm' button appeared.")
                realistic_click(confirm_location)
                time.sleep(random.uniform(1.5, 3.9))
                return True
        except Exception as e:
            print(f"⚠️ Confirm button check failed: {e}")

        print("❌ 'Confirm' not found. Retrying 'sign'...")

    return False

# === Wait before starting ===
print("⌛ You have 5 seconds to switch to the app...")
time.sleep(5)

# === Main Loop ===
while not stop_flag:
    i = 0
    while i < len(BUTTON_IMAGES):
        if stop_flag:
            break

        current_img = BUTTON_IMAGES[i]
        image_name = current_img.lower()

        if 'sign' in image_name:
            confirm_img = BUTTON_IMAGES[i + 1]  # next is confirm
            success = click_sign_and_wait_for_confirm(current_img, confirm_img)
            if not success:
                break
            i += 1  # skip to confirm step now
        else:
            find_and_click_button(current_img)

        i += 1

    if not stop_flag:
        delay = random.uniform(2, 7)
        print(f"🔁 One cycle completed. Waiting {delay:.2f}s before next cycle...\n")
        time.sleep(delay)

print("✅ Script ended successfully.")
