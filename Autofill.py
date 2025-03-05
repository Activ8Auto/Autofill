from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime
import Dict


MAX_RETRIES = 5  # Maximum number of full script retries
total_minutes = 0


def fill_form(selected_date, run_headless):
    global total_minutes
    diagnoses = {
        "ADHD-1": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Dextroamphetamine-amphetamine 20 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-2": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Adderall XR 30 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-3": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Vyvanse 40 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-4": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Methylphenidate ER 18 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-5": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Atomoxetine 100 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-6": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Atomoxetine 100 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-7": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Vyvanse 60 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-8": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Vyvanse 60 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "ADHD-9": {
            "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
            "current_medications": ["ADHD Medications"],
            "medications":["Vyvanse 40 mg; "],
            "exclusion_group":"ADHD"
        
        },
        "Major Depressive Disorder-1":{
            "icd_code": "ICD-10 - F320 - Major depressive disorder",
            "current_medications": ["Antidepressants"],
            "medications":["Auvelity 45 mg-105 mg; "],
            "exclusion_group":"MDD"
        },
        "Major Depressive Disorder-2":{
            "icd_code": "ICD-10 - F320 - Major depressive disorder",
            "current_medications": ["Antidepressants"],
            "medications":["Sertraline 100 mg; "],
            "exclusion_group":"MDD"
        },
        "Major Depressive Disorder-3":{
            "icd_code": "ICD-10 - F320 - Major depressive disorder",
            "current_medications": ["Antidepressants"],
            "medications":["Lexapro 20 mg; ", "Wellbutrin xl 150 mg;  "],
            "exclusion_group":"MDD"
        },
        "Major Depressive Disorder-4":{
            "icd_code": "ICD-10 - F320 - Major depressive disorder",
            "current_medications": ["Antidepressants"],
            "medications":["Prozac 40 mg; "],
            "exclusion_group":"MDD"
        },
        "Bipolar-1-1":{
            "icd_code": "ICD-10 - F310 - Bipolar disorder",
            "current_medications": ["Antidepressants", "Antipsychotics"],
            "medications":["Lithium 300 mg; "],
            "exclusion_group":"Bipolar"
        },
        "Bipolar-1-2":{
            "icd_code": "ICD-10 - F310 - Bipolar disorder",
            "current_medications": ["Antidepressants", "Antipsychotics"],
            "medications":["Lamictal 50 mg; "],
            "exclusion_group":"Bipolar"
        },
        "Bipolar-1-3":{
            "icd_code": "ICD-10 - F310 - Bipolar disorder",
            "current_medications": ["Antidepressants", "Antipsychotics"],
            "medications":["Carbamazepine 300 mg; "],
            "exclusion_group":"Bipolar"
        },
        "Bipolar-2-1":{
            "icd_code": "ICD-10 - F3181 - Bipolar II disorder",
            "current_medications": ["Antipsychotics"],
            "medications":["Lithium 300mg; "],
            "exclusion_group":"Bipolar"
        },
         "Bipolar-2-2":{
            "icd_code": "ICD-10 - F3181 - Bipolar II disorder",
            "current_medications": ["Antipsychotics"],
            "medications":["Vraylar 3mg; "],
            "exclusion_group":"Bipolar"
        },
        "Bipolar-2-3":{
            "icd_code": "ICD-10 - F3181 - Bipolar II disorder",
            "current_medications": ["Antipsychotics"],
            "medications":["Latuda 20 mg; "],
            "exclusion_group":"Bipolar"
        },
        "Generalized Anxiety Disorder-1":{
            "icd_code": "ICD-10 - F411 - Generalized anxiety disorder",
            "current_medications": ["Antianxiety Medications"],
            "medications":["Hydroxyzine pamoate 25 mg; ", "Gabapentin 300 mg; ", "Propranolol 10 mg; "],
            "exclusion_group":"Anxiety"
        },
        "Generalized Anxiety Disorder-2":{
            "icd_code": "ICD-10 - F411 - Generalized anxiety disorder",
            "current_medications": ["Antianxiety Medications", "Antidepressants"],
            "medications":["QUEtiapine 100 mg; ", "Propranolol 10 mg; "],
            "exclusion_group":"Anxiety"
        },
         "Generalized Anxiety Disorder-3":{
            "icd_code": "ICD-10 - F411 - Generalized anxiety disorder",
            "current_medications": ["Antianxiety Medications", "Antidepressants"],
            "medications":["Paroxetine 20 mg; ", "Buspirone 20 mg; "],
            "exclusion_group":"Anxiety"
        },
         "Generalized Anxiety Disorder-4":{
            "icd_code": "ICD-10 - F411 - Generalized anxiety disorder",
            "current_medications": ["Antianxiety Medications", "Antidepressants"],
            "medications":["Duloxetine 60 mg; "],
            "exclusion_group":"Anxiety"
        },
        "Post-Traumatic Stress":{
            "icd_code": "ICD-10 - F4310 - Post-traumatic stress disorder",
            "current_medications": ["Antianxiety Medications"],
            "medications":["Sertraline 100 mg; "],
            "exclusion_group":"PTSD"
        },
        "Schizophrenia-1":{
            "icd_code": "ICD-10 - F209 - Schizophrenia",
            "current_medications": ["Antipsychotics"],
            "medications":["Risperidone 2 mg; "],
            "exclusion_group":"Bipolar"
        },
    

        }
    def select_random_diagnoses(diagnoses, max_diagnoses=3):
        """
        Selects up to `max_diagnoses` ensuring no conflicting exclusions.
        """
        selected_diagnoses = []
        seen_groups = set()

        # Shuffle list of diagnoses to ensure randomness
        shuffled_diagnoses = list(diagnoses.items())
        random.shuffle(shuffled_diagnoses)

        for diag_name, diag_info in shuffled_diagnoses:
            group = diag_info["exclusion_group"]

            # If diagnosis belongs to an exclusion group, ensure only one is picked per group
            if group and group in seen_groups:
                continue  # Skip this diagnosis since another from the group is already picked

            # Add the diagnosis to the final selection
            selected_diagnoses.append((diag_name, diag_info))
            
            # Track exclusion groups
            if group:
                seen_groups.add(group)

            # Stop when we reach max allowed diagnoses
            if len(selected_diagnoses) >= max_diagnoses:
                break

        return selected_diagnoses




    """
    Automates form filling with error handling.
    If Preceptor selection fails, the script restarts from the beginning.
    """
    
    for attempt in range(MAX_RETRIES):
        with sync_playwright() as p:
            try:
                print(f"🔄 Full Script Attempt {attempt + 1}/{MAX_RETRIES}...")

                browser = p.chromium.launch_persistent_context(
                    user_data_dir="C://Users//tjand//AppData//Local//Microsoft//Edge//User Data",  
                    channel="msedge",
                    headless=run_headless,
                    args=[
                            "--window-position=0,0",  # Force browser to top-left
                            "--window-size=2560,1440",
                            "--force-device-scale-factor=1",
                            "--disable-features=CalculateNativeWinOcclusion"  # Prevents Edge from resizing unexpectedly
                            
                        ]
                    )
                page = browser.new_page()
                page.set_viewport_size({"width": 2560, "height": 1440})


            

                # ✅ Open the webpage
                page.goto("https://cu.medtricslab.com/cases/create/14/")  

                # ✅ Select Date
                page.click("input[placeholder='Case Date']")
                page.click(f"text='{selected_date}'")
                page.wait_for_timeout(500)

                # ✅ Select Faculty Preceptor
                page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/input')
                page.click("text='Veronica Wright (Faculty) EN:D41297586 (Faculty)'")

                # Duration Selection Logic
                duration_options = ["30 Minutes", "1 Hour"]
                visit_types = ["Follow up Client Encounter", "New Client Encounter"]
                

                duration_weights = [0.9, 0.1]

                random_duration = random.choices(duration_options, weights=duration_weights, k=1)[0]
                temp_minutes = 60 if random_duration == "1 Hour" else 30

                random_visit_type = "New Admit" if random_duration == "1 Hour" else "Follow up Client Encounter"
    
                    
                    #Duration 

                # page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input')
                # page.wait_for_selector(f"text='1 Hour'")
                # page.click("text='1 Hour'")

                page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input')
                page.wait_for_selector(f"text='{random_duration}'")
                page.click(f"text='{random_duration}'")
                print(f"Duration: ⏳ {random_duration}")
                # Select Preceptor (with Retry Logic)
                if not select_preceptor(page):
                    print("🚨 Preceptor selection failed after retries. Restarting full script...")
                    
                    continue  # Restart the entire script from the beginning
        

               

                page.locator(".vue-treeselect__multi-value").nth(1).click()
                dropdown = page.locator(".vue-treeselect--open")  # Locate the active dropdown
                
                # Diagnosis
                max_diagnoses = random.randint(1, 3)  # Randomly pick 1, 2, or 3 diagnoses
                selected_diagnoses = select_random_diagnoses(diagnoses, max_diagnoses=max_diagnoses)

                
                dropdown = page.locator(".vue-treeselect--open")

                for _, diag_info in selected_diagnoses:
                    icd_code = diag_info["icd_code"]
                    dropdown.locator(".vue-treeselect__input").fill(icd_code)
                    print(f"ICD Choosen: 🏷️{icd_code}")
                    page.wait_for_timeout(500)
                    dropdown.locator(".vue-treeselect__option", has_text=icd_code).click()
                    page.wait_for_timeout(500) 
                    # dropdown.locator(".vue-treeselect__input").fill("")
                    # page.wait_for_timeout(500) 
    
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

                for medication in all_medications:
                    dropdown = page.locator(".vue-treeselect--open")  # Locate the active dropdown
                    dropdown.locator(".vue-treeselect__input").fill(medication)  # Type medication
                    page.wait_for_timeout(500)
                    dropdown.locator(".vue-treeselect__option", has_text=medication).click()  # Click matching option
                    page.wait_for_timeout(300) 

                #Student prescribed meds
                page.locator(".vue-treeselect__multi-value").nth(6).click()
                page.wait_for_timeout(500)  # Allow dropdown to open
                meds_dropdown = page.locator(".vue-treeselect--open")
                meds_dropdown.locator(".vue-treeselect__input").fill("N/A")
                page.wait_for_timeout(500)
                na_option = meds_dropdown.locator(".vue-treeselect__option", has_text="N/A")
                na_option.wait_for(state="visible", timeout=1000)  # Wait until it's visible
                na_option.click()       
                page.click("body")
    

                # Teaching/Support by Student
                page.locator(".vue-treeselect__multi-value").nth(9).click()
                page.wait_for_timeout(500)
                page.click("text='Medication Education and Management'")
                page.click("body")

                # Age
                ages = ["13-17 years","22-35 years", "18-21 years","36-55 years","56-64 years","65-75 years","76-85 years"]
                age_weight = [0.1, 0.3, 0.2, 0.2, 0.1, 0.05, 0.05]
                random_age = random.choices(ages, weights = age_weight)[0]
                print(f"Age Range: 🎂 {random_age}")

                page.locator(".vue-treeselect--single").nth(2).click()
                page.wait_for_timeout(500)
                page.click(f"text='{random_age}'")
                page.click("body")

                #Gender
                gender = ["Male", "Female","Transgender man/trans man","Transgender woman/trans woman"]
                gender_weight = [0.475, 0.475, 0.025, 0.025]
                random_gender = random.choices(gender,weights=gender_weight)[0]
                print(f"Gender: ⚤ {random_gender}")

                page.locator(".vue-treeselect__multi-value").nth(11).click()
                page.wait_for_timeout(500)
                page.click(f"text='{random_gender}'")
                #page.click("body")

                # Race
                races=["Caucasian", "African American","Hispanic","Asian"]
                weights = [0.75, 0.05, 0.15, 0.05]
                random_race = random.choices(races, weights=weights, k=1)[0]
                print(f"Race: 🌎 {random_race}")
                
                page.locator(".vue-treeselect--single").nth(3).click()
                page.wait_for_timeout(500)
                page.click(f"text='{random_race}'")
                page.click("body")

                # ✅ Fill out the textarea
                all_prescribed_meds = set()
                for _, diag_info in selected_diagnoses:
                    all_prescribed_meds.update(diag_info["medications"])  # Deduplicate medications
                
                prescribed_meds = "".join(all_prescribed_meds)
                print(f"💊 Medications Entered: {prescribed_meds}")
                page.fill("textarea.form-control", prescribed_meds)
                
                

            


                #Visit Mode

                page.locator(".vue-treeselect--single").nth(4).click()
                page.wait_for_timeout(500)
                page.click("text='Face to Face'")
                page.click("body")

                #Site Type
                page.locator(".vue-treeselect--single").nth(5).click()
                page.wait_for_timeout(500)
                page.click("text='Outpatient'")
                page.click("body")

                #Encounter Type
                page.locator(".vue-treeselect--single").nth(6).click()
                page.wait_for_timeout(500)
                page.click(f"text='{random_visit_type}'")
                print(f"Visit Type: 🏥 {random_visit_type}")
                page.click("body")

                #Site Location
                page.locator(".vue-treeselect--single").nth(7).click()
                page.wait_for_timeout(500)
                page.click("text='Outpatient Clinic'")
                page.click("body")
                #CPT Visit Code
                # Select input field using CSS selector and fill it with "99214"
                # Find all input fields with class "form-control"
                page.locator("input.form-control").nth(13).fill("99215")
             


                # page.fill("input.form-control", "99214")


                #Student Level of Function
                page.locator(".vue-treeselect--single").nth(9).click()
                page.wait_for_timeout(500)
                page.click("text='25% Student/75% Preceptor'")
                page.click("body")

                #Client Complexity 
                page.locator(".vue-treeselect--single").nth(8).click()
                page.wait_for_timeout(500)
                page.click("text='Moderate complexity (multiple acute or chronic issues that require ongoing intervention, stable, responsive to treatments)'")
                page.click("body")


                print("✅ Form completed successfully!")
                page.click("//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]")
                total_minutes += temp_minutes
                return  # ✅ Exit the script if it runs successfully

            except Exception as e:
                print(f"❌ Error during attempt {attempt + 1}: {e}")
                print("🔄 Restarting full script...")

    print("🚨 Max retries reached. Exiting...")

def select_preceptor(page):
    """
    Tries to select the correct Preceptor. If incorrect names appear, refresh the page and retry.
    """
    MAX_RETRIES = 1
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 Attempting to select Preceptor...")

            # ✅ Click the Preceptor dropdown
            page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div')

            # ✅ Type "Ali" to filter preceptors
            page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "A")
            page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "l")
            page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "i")

            # ✅ Wait for the correct Preceptor to appear
            page.wait_for_selector("text='Alison Baker (Preceptor) EN:0034U00003CyIP8QAN (Preceptor)'", state="visible", timeout=1000)

            # ✅ Click the correct Preceptor
            page.click("text='Alison Baker (Preceptor) EN:0034U00003CyIP8QAN (Preceptor)'")

            print("✅ Preceptor selected successfully!")
            return True  # ✅ Success: Preceptor was selected

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")

            if attempt < MAX_RETRIES - 1:
                print("🔄 Refreshing page and retrying preceptor selection...")
                page.reload()
                page.wait_for_timeout(1000)  # Wait for page to reload
            else:
                print("🚨 Max preceptor selection retries reached.")
                return False  # ✅ Only restart script if preceptor fails

if __name__ == "__main__":
    RUN_COUNT = int(input("🔢 Enter how many times you want the script to run: "))
    selected_date = input("📅 Enter the date you want to select (e.g., '12'): ").strip()
    run_headless = input("👀 Do you want to see the browser while it runs? (y/n): ").strip().lower() == "n"
    total_finished_hours = total_minutes // 60
    total_finished_minutes = total_minutes % 60
    
    for i in range(RUN_COUNT):
        print(f"🚀 Starting Run {i+1}/{RUN_COUNT} with date {selected_date}...")
        fill_form(selected_date, run_headless)

        if i < RUN_COUNT - 1:  # Avoid sleeping after the last run
                wait_time = random.randint(60, 120)  # Random wait time between 4 to 6 minutes
                finished_time = datetime.now().strftime("%I:%M %p MST")
                total_hours = total_minutes // 60
                remaining_minutes = total_minutes % 60
                print(f"✅ Run {i+1}/{RUN_COUNT} finished at {finished_time}. ⏳ Waiting {wait_time // 60} minutes and {wait_time % 60} seconds before next run. 🕒 Total Duration for {total_hours} hours and {remaining_minutes} minutes")
                time.sleep(wait_time)
    print(f"✅ All runs completed successfully! Total time {total_hours} hours and {remaining_minutes} minutes ")
   
# from playwright.sync_api import sync_playwright
# import time
# import random
# from datetime import datetime
# import sys

# MAX_RETRIES = 5  # Maximum number of full script retries
# total_minutes = 0

# def fill_form(selected_date, run_headless):
#     global total_minutes
#     diagnoses = {
#         "ADHD-1": {
#             "icd_code": "ICD-10 - F900 - Attention-deficit hyperactivity disorder",
#             "current_medications": ["ADHD Medications"],
#             "medications":["Dextroamphetamine-amphetamine 20 mg; "],
#             "exclusion_group":"ADHD"
#         },
#         # ... [Your existing diagnoses dictionary remains unchanged] ...
#         "Schizophrenia-1":{
#             "icd_code": "ICD-10 - F209 - Schizophrenia",
#             "current_medications": ["Antipsychotics"],
#             "medications":["Risperidone 2 mg; "],
#             "exclusion_group":"Bipolar"
#         },
#     }

#     def select_random_diagnoses(diagnoses, max_diagnoses=3):
#         """
#         Selects up to `max_diagnoses` ensuring no conflicting exclusions.
#         """
#         selected_diagnoses = []
#         seen_groups = set()
#         shuffled_diagnoses = list(diagnoses.items())
#         random.shuffle(shuffled_diagnoses)

#         for diag_name, diag_info in shuffled_diagnoses:
#             group = diag_info["exclusion_group"]
#             if group and group in seen_groups:
#                 continue
#             selected_diagnoses.append((diag_name, diag_info))
#             if group:
#                 seen_groups.add(group)
#             if len(selected_diagnoses) >= max_diagnoses:
#                 break
#         return selected_diagnoses

#     for attempt in range(MAX_RETRIES):
#         with sync_playwright() as p:
#             try:
#                 print(f"🔄 Full Script Attempt {attempt + 1}/{MAX_RETRIES}...")
#                 browser = p.chromium.launch_persistent_context(
#                     user_data_dir="C://Users//tjand//AppData//Local//Microsoft//Edge//User Data",  
#                     channel="msedge",
#                     headless=run_headless,
#                     args=[
#                         "--window-position=0,0",
#                         "--window-size=2560,1440",
#                         "--force-device-scale-factor=1",
#                         "--disable-features=CalculateNativeWinOcclusion"
#                     ]
#                 )
#                 page = browser.new_page()
#                 page.set_viewport_size({"width": 2560, "height": 1440})

#                 page.goto("https://cu.medtricslab.com/cases/create/14/")
#                 page.click("input[placeholder='Case Date']")
#                 page.click(f"text='{selected_date}'")
#                 page.wait_for_timeout(500)

#                 page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/input')
#                 page.click("text='Veronica Wright (Faculty) EN:D41297586 (Faculty)'")

#                 duration_options = ["30 Minutes", "1 Hour"]
#                 duration_weights = [0.9, 0.1]
#                 random_duration = random.choices(duration_options, weights=duration_weights, k=1)[0]
#                 temp_minutes = 60 if random_duration == "1 Hour" else 30
#                 random_visit_type = "New Admit" if random_duration == "1 Hour" else "Follow up Client Encounter"

#                 page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input')
#                 page.wait_for_selector(f"text='{random_duration}'")
#                 page.click(f"text='{random_duration}'")
#                 print(f"Duration: ⏳ {random_duration}")

#                 if not select_preceptor(page):
#                     print("🚨 Preceptor selection failed after retries. Restarting full script...")
#                     continue

#                 # ... [Rest of your form filling logic remains unchanged] ...

#                 print("✅ Form completed successfully!")
#                 # page.click("//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]")
#                 total_minutes += temp_minutes
#                 return

#             except Exception as e:
#                 print(f"❌ Error during attempt {attempt + 1}: {e}")
#                 print("🔄 Restarting full script...")
#     print("🚨 Max retries reached. Exiting...")

# def select_preceptor(page):
#     MAX_RETRIES = 1
#     for attempt in range(MAX_RETRIES):
#         try:
#             print(f"🔄 Attempting to select Preceptor...")
#             page.click('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div')
#             page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "A")
#             page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "l")
#             page.press('xpath=//*[@id="content"]/div[2]/div/div/div[2]/div/div[2]/div[3]/div/div/div[1]/div[1]/div', "i")
#             page.wait_for_selector("text='Alison Baker (Preceptor) EN:0034U00003CyIP8QAN (Preceptor)'", state="visible", timeout=1000)
#             page.click("text='Alison Baker (Preceptor) EN:0034U00003CyIP8QAN (Preceptor)'")
#             print("✅ Preceptor selected successfully!")
#             return True
#         except Exception as e:
#             print(f"❌ Attempt {attempt + 1} failed: {e}")
#             if attempt < MAX_RETRIES - 1:
#                 print("🔄 Refreshing page and retrying preceptor selection...")
#                 page.reload()
#                 page.wait_for_timeout(1000)
#             else:
#                 print("🚨 Max preceptor selection retries reached.")
#                 return False

# def countdown(wait_time):
#     """Display a countdown timer until the next run."""
#     remaining_time = wait_time
#     while remaining_time > 0:
#         mins, secs = divmod(remaining_time, 60)
#         timer = f"\033[1m⏳ Next run in: {mins:02d} minutes {secs:02d} seconds\033[0m"
#         sys.stdout.write(f"\r{timer}")
#         sys.stdout.flush()
#         time.sleep(1)
#         remaining_time -= 1
#     sys.stdout.write("\r\033[K")  # Clear the line after countdown
#     sys.stdout.flush()

# if __name__ == "__main__":
#     RUN_COUNT = int(input("🔢 Enter how many times you want the script to run: "))
#     selected_date = input("📅 Enter the date you want to select (e.g., '12'): ").strip()
#     run_headless = input("👀 Do you want to see the browser while it runs? (y/n): ").strip().lower() == "n"
    
#     for i in range(RUN_COUNT):
#         print(f"🚀 Starting Run {i+1}/{RUN_COUNT} with date {selected_date}...")
#         fill_form(selected_date, run_headless)

#         if i < RUN_COUNT - 1:  # Avoid waiting after the last run
#             wait_time = random.randint(10, 15)  # Random wait time between 1 to 2 minutes
#             finished_time = datetime.now().strftime("%I:%M %p MST")
#             total_hours = total_minutes // 60
#             remaining_minutes = total_minutes % 60
#             print(f"✅ Run {i+1}/{RUN_COUNT} finished at {finished_time}. 🕒 Total Duration: {total_hours} hours and {remaining_minutes} minutes")
#             countdown(wait_time)
#             print(f"🚀 Preparing for Run {i+2}/{RUN_COUNT}...")

#     total_hours = total_minutes // 60
#     remaining_minutes = total_minutes % 60
#     print(f"✅ All runs completed successfully! Total time: {total_hours} hours and {remaining_minutes} minutes")