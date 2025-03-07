from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime
from mental_health_dict import diagnoses

# Global variables
MAX_RETRIES = 5  # Maximum number of full script retries
total_minutes = 0
browser_context = None
playwright_instance = None



def select_random_diagnoses(diagnoses, max_diagnoses=3):
    selected_diagnoses = []
    seen_groups = set()
    shuffled_diagnoses = list(diagnoses.items())
    random.shuffle(shuffled_diagnoses)

    for diag_name, diag_info in shuffled_diagnoses:
        group = diag_info["exclusion_group"]
        if group and group in seen_groups:
            continue
        selected_diagnoses.append((diag_name, diag_info))
        if group:
            seen_groups.add(group)
        if len(selected_diagnoses) >= max_diagnoses:
            break
    return selected_diagnoses

def auto_sign_in(page):
    try:
        if page.locator("a.btn.btn-danger[href='/sso/login/saml/?idp=cu']").count() > 0:
            print("🔁 Redirecting to login page...")
            page.click("a.btn.btn-danger[href='/sso/login/saml/?idp=cu']")
            page.fill("input[name='identifier']", "D41270944")
            page.wait_for_timeout(1000)
            page.fill("input[name='credentials.passcode']", "CoolCow02251990!")
            page.click("input.button.button-primary[type='submit']")
            page.wait_for_timeout(3000)
            page.click("a.button.select-factor.link-button[aria-label='Select to get a push notification to the Okta Verify app.']")
            page.click("input.button.button-primary[type='submit'][value='Send push']")
            if "dashboard" in page.url or "home" in page.url:
                print("✅ Successfully logged in!")
            else:
                print("⚠️ Login might have failed or was unnecessary.")
        else:
            print("🔓 No login page detected. Continuing...")
    except Exception as e:
        print(f"❌ Error in auto-sign-in: {e}")

def select_preceptor(page):
    MAX_PRECEPTOR_RETRIES = 1
    for attempt in range(MAX_PRECEPTOR_RETRIES):
        try:
            print(f"🔄 Attempting to select Preceptor (Attempt {attempt + 1}/{MAX_PRECEPTOR_RETRIES})...")
            page.locator(".vue-treeselect__multi-value").nth(0).click()
            page.wait_for_timeout(1000)
            page.click("text='Angel Julmy (Preceptor) EN:0034U00003Jw7FaQAJ (Preceptor)'")
            print("✅ Preceptor selected successfully!")
            return True
        except Exception as e:
            print(f"❌ Preceptor selection failed: {e}")
            if attempt < MAX_PRECEPTOR_RETRIES - 1:
                print("🔄 Refreshing page and retrying...")
                page.reload()
                page.wait_for_timeout(1000)
            else:
                print("🚨 Max preceptor retries reached.")
                return False

def fill_form(selected_date, run_headless, test=False):
    global total_minutes, browser_context, playwright_instance
    print(f"DEBUG: Entering fill_form with total_minutes = {total_minutes}")

    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 Full Script Attempt {attempt + 1}/{MAX_RETRIES}...")
            if not playwright_instance:
                playwright_instance = sync_playwright().start()
            browser_context = playwright_instance.chromium.launch_persistent_context(
                user_data_dir="C://Users//tjand//AppData//Local//Microsoft//Edge//User Data",
                channel="msedge",
                headless=run_headless,
                args=[
                    "--window-position=0,0",
                    "--window-size=2560,1440",
                    "--force-device-scale-factor=1",
                    "--disable-features=CalculateNativeWinOcclusion"
                ]
            )
            page = browser_context.new_page()
            page.set_viewport_size({"width": 2560, "height": 1440})

            page.goto("https://cu.medtricslab.com/cases/create/14/")
            auto_sign_in(page)
            page.wait_for_timeout(2000)

            # Date
            page.click("input[placeholder='Case Date']")
            page.click(f"text='{selected_date}'")
            page.wait_for_timeout(1000)

            # Scheduled Rotation
            page.locator(".vue-treeselect__input").nth(0).click()
            page.wait_for_timeout(500)
            page.click("text='NR605-66257-Outpatient Psychiatric Clinic-National Mental Health-Julmy (Mar 03, 2025 - Apr 26, 2025) - Taylor Andrews'")

            # Faculty Preceptor
            page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/input')
            page.click("text='Kimberly Sena (Faculty) EN:D41258501 (Faculty)'")

            # Duration and Visit Type
            duration_options = ["30 Minutes", "1 Hour"]
            duration_weights = [0.8, 0.2]
            random_duration = random.choices(duration_options, weights=duration_weights, k=1)[0]
            temp_minutes = 60 if random_duration == "1 Hour" else 30
            random_visit_type = "New Client Encounter" if random_duration == "1 Hour" else "Follow up Client Encounter"
            page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input')
            page.wait_for_selector(f"text='{random_duration}'")
            page.wait_for_timeout(500)
            page.click(f"text='{random_duration}'")
            print(f"Duration: ⏳ {random_duration}")

            # Preceptor Selection
            if not select_preceptor(page):
                print("🚨 Preceptor selection failed after retries. Restarting...")
                browser_context.close()
                continue

            # Diagnosis
            max_diagnoses = random.randint(1, 3)
            selected_diagnoses = select_random_diagnoses(diagnoses, max_diagnoses=max_diagnoses)
            page.locator(".vue-treeselect__multi-value").nth(1).click()
            dropdown = page.locator(".vue-treeselect--open")
            for _, diag_info in selected_diagnoses:
                icd_code = diag_info["icd_code"]
                dropdown.locator(".vue-treeselect__input").fill(icd_code)
                print(f"ICD Chosen: 🏷️ {icd_code}")
                page.wait_for_timeout(500)
                dropdown.locator(".vue-treeselect__option", has_text=icd_code).click()
                page.wait_for_timeout(500)
            page.click("body")

            # Physical Exam
            page.locator(".vue-treeselect__multi-value").nth(3).click()
            page.wait_for_timeout(500)
            page.click("text='N/A'")
            page.click("body")

            # Current Medications
            page.locator(".vue-treeselect__multi-value").nth(5).click()
            page.wait_for_timeout(500)
            all_medications = set()
            for _, diag_info in selected_diagnoses:
                all_medications.update(diag_info["current_medications"])
            print(f"⚕️ Medications to Select: {all_medications}")
            dropdown = page.locator(".vue-treeselect--open")
            for medication in all_medications:
                dropdown.locator(".vue-treeselect__input").fill(medication)
                page.wait_for_timeout(500)
                dropdown.locator(".vue-treeselect__option", has_text=medication).click()
                page.wait_for_timeout(300)

            # Student Prescribed Meds
            page.locator(".vue-treeselect__multi-value").nth(6).click()
            page.wait_for_timeout(500)
            meds_dropdown = page.locator(".vue-treeselect--open")
            meds_dropdown.locator(".vue-treeselect__input").fill("N/A")
            page.wait_for_timeout(500)
            meds_dropdown.locator(".vue-treeselect__option", has_text="N/A").click()
            page.click("body")

            # Teaching/Support by Student
            page.locator(".vue-treeselect__multi-value").nth(9).click()
            page.wait_for_timeout(500)
            page.click("text='Medication Education and Management'")
            page.click("body")

            # Age
            ages = ["13-17 years", "22-35 years", "18-21 years", "36-55 years", "56-64 years", "65-75 years", "76-85 years"]
            age_weight = [0.1, 0.3, 0.2, 0.2, 0.1, 0.05, 0.05]
            random_age = random.choices(ages, weights=age_weight)[0]
            page.locator(".vue-treeselect--single").nth(3).click()
            page.wait_for_timeout(500)
            page.click(f"text='{random_age}'")
            page.click("body")
            print(f"Age Range: 🎂 {random_age}")

            # Gender
            gender = ["Male", "Female", "Transgender man/trans man", "Transgender woman/trans woman"]
            gender_weight = [0.475, 0.475, 0.025, 0.025]
            random_gender = random.choices(gender, weights=gender_weight)[0]
            page.locator(".vue-treeselect__multi-value").nth(11).click()
            page.wait_for_timeout(500)
            page.click(f"text='{random_gender}'")
            print(f"Gender: ⚤ {random_gender}")

            # Race
            races = ["Caucasian", "African American", "Hispanic", "Asian"]
            weights = [0.75, 0.05, 0.15, 0.05]
            random_race = random.choices(races, weights=weights, k=1)[0]
            page.locator(".vue-treeselect--single").nth(4).click()
            page.wait_for_timeout(500)
            page.click(f"text='{random_race}'")
            page.click("body")
            print(f"Race: 🌎 {random_race}")

            # Medications Textarea
            all_prescribed_meds = set()
            for _, diag_info in selected_diagnoses:
                all_prescribed_meds.update(diag_info["medications"])
            prescribed_meds = "".join(all_prescribed_meds)
            print(f"💊 Medications Entered: {prescribed_meds}")
            page.fill("textarea.form-control", prescribed_meds)

            # Visit Mode
            page.locator(".vue-treeselect--single").nth(5).click()
            page.wait_for_timeout(500)
            page.click("text='Face to Face'")
            page.click("body")

            # Site Type
            page.locator(".vue-treeselect--single").nth(6).click()
            page.wait_for_timeout(500)
            page.click("text='Outpatient'")
            page.click("body")

            # Encounter Type
            page.locator(".vue-treeselect--single").nth(7).click()
            page.wait_for_timeout(500)
            page.click(f"text='{random_visit_type}'")
            print(f"Visit Type: 🏥 {random_visit_type}")
            page.click("body")

            # Site Location
            page.locator(".vue-treeselect--single").nth(8).click()
            page.wait_for_timeout(500)
            page.click("text='Outpatient Clinic'")
            page.click("body")

            # CPT Visit Code
            page.locator("input.form-control").nth(13).fill("99215")

            # Student Level of Function
            page.locator(".vue-treeselect--single").nth(10).click()
            page.wait_for_timeout(500)
            page.click("text='25% Student/75% Preceptor'")
            page.click("body")

            # Client Complexity
            page.locator(".vue-treeselect--single").nth(9).click()
            page.wait_for_timeout(500)
            page.click("text='Moderate complexity (multiple acute or chronic issues that require ongoing intervention, stable, responsive to treatments)'")
            page.click("body")

            # Save or Skip
            print("✅ Form completed successfully!")
            if not test:
                page.click("//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]")
                print("✅ Saved form submission")
            else:
                print("✅ Test mode: Save button not clicked")

            total_minutes += temp_minutes
            print(f"DEBUG: After increment, total_minutes = {total_minutes}")
            return  # Success, exit retry loop

        except Exception as e:
            print(f"❌ Error during attempt {attempt + 1}: {e}")
            if browser_context:
                browser_context.close()
                browser_context = None
            if attempt == MAX_RETRIES - 1:
                print("🚨 Max retries reached. Exiting...")
                raise
            print("🔄 Restarting full script...")

def cancel_automation():
    global browser_context, playwright_instance
    if browser_context:
        browser_context.close()
        browser_context = None
        print("Browser context closed.")
    if playwright_instance:
        playwright_instance.stop()
        playwright_instance = None
        print("Playwright instance stopped.")

if __name__ == "__main__":
    while True:
        try:
            target_hours = float(input("⏰ Enter the target total time in hours (e.g., 4): "))
            if target_hours <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    TARGET_TOTAL_MINUTES = int(target_hours * 60)
    print(f"Script will run until total time reaches or exceeds {target_hours} hours ({TARGET_TOTAL_MINUTES} minutes).")

    selected_date = input("📅 Enter the date you want to select (e.g., '12'): ").strip()
    run_headless = input("👀 Do you want to see the browser while it runs? (y/n): ").strip().lower() == "n"

    while True:
        try:
            min_wait = int(input("⏳ Enter the minimum wait time between runs in seconds: "))
            break
        except ValueError:
            print("Please enter an integer value.")

    while True:
        try:
            max_wait = int(input("⏳ Enter the maximum wait time between runs in seconds: "))
            break
        except ValueError:
            print("Please enter an integer value.")

    a = min(min_wait, max_wait)
    b = max(min_wait, max_wait)
    print(f"Wait time between runs will be randomly chosen between {a} and {b} seconds.")

    run_counter = 0
    while total_minutes < TARGET_TOTAL_MINUTES:
        try:
            run_counter += 1
            print(f"🚀 Starting Run {run_counter} with date {selected_date} (Current total: {total_minutes} minutes)...")
            fill_form(selected_date, run_headless)
            print(f"DEBUG: Total minutes after run {run_counter} = {total_minutes}")

            if total_minutes < TARGET_TOTAL_MINUTES:
                wait_time = random.randint(a, b)
                finished_time = datetime.now().strftime("%I:%M %p MST")
                total_hours = total_minutes // 60
                remaining_minutes = total_minutes % 60
                print(f"✅ Run {run_counter} finished at {finished_time}. ⏳ Waiting {wait_time // 60} minutes and {wait_time % 60} seconds before next run. 🕒 Current Total: {total_hours} hours and {remaining_minutes} minutes")
                time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Error after run {run_counter}: {e}")
            break

    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    print(f"✅ All runs completed successfully! Total time reached: {total_hours} hours and {remaining_minutes} minutes (Target was {target_hours} hours)")
    cancel_automation()  # Clean up after standalone run