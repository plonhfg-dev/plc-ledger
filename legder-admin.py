#!/data/data/com.termux/files/usr/bin/python3
import json
import os
import random
from collections import defaultdict

DB_FILE = 'database.json'

# DEFCON Security Status Dictionary
STATUS_LEVELS = {
    "1": "Clean - Verified Valid",
    "2": "FLAGGED - Suspicious / Pending Audit",
    "3": "FLAGGED - Stolen / Do Not Honor",
    "4": "FLAGGED - Counterfeit / Known Forgery",
    "5": "Burned - Removed from Circulation"
}

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("[!] ERROR: Corrupted JSON file. Starting fresh.")
            return {}

def save_db(data):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print("[+] SYSTEM: Ledger saved successfully to database.json")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_status():
    print("\n--- SECURITY STATUS ADJUSTER ---")
    for key, val in STATUS_LEVELS.items():
        print(f"{key}. {val}")
    choice = input("Select Status Level (1-5) [Default: 1]: ").strip()
    return STATUS_LEVELS.get(choice, STATUS_LEVELS["1"])

def get_common_mint_data():
    amount = input("Enter Denomination Amount (e.g., 100): ").strip()
    
    is_forever = input("Is this a Forever Note? (y/n): ").strip().lower()
    if is_forever == 'y':
        note_type = "Forever PLC"
        expiry = "N/A (Never Expires)"
        img_path = f"images/plc_{amount}_forever.jpg"
    else:
        note_type = "Time Limited PLC"
        expiry = input("Enter Expiry Date (e.g., '15 June 2026'): ").strip()
        img_path = f"images/plc_{amount}_limited.jpg"

    area = input("Enter Local Area / Issued To: ").strip()
    status = select_status()
    
    return amount, note_type, expiry, img_path, area, status

def main():
    db = load_db()

    while True:
        print("\n" + "="*50)
        print("   PLONHFG CENTRAL BANK - ERP ROOT ACCESS v5.0")
        print("="*50)
        print("1. [MINT] Single Note Generation")
        print("2. [BULK MINT] Mass Assembly Line")
        print("3. [MOVE] Update Location (Single/Bulk)")
        print("4. [SECURE] Adjust Threat Status (Single/Bulk)")
        print("5. [QA] Mint Correction (Fix Prefix Collisions)")
        print("6. [DASHBOARD] Hierarchical Asset Analytics")
        print("7. [DUMP] View Raw JSON Ledger")
        print("8. [EDIT] Modify Existing Note Details")
        print("9. [EXIT] Save and Shutdown Terminal")
        print("="*50)
        
        choice = input("root@plonhfg-vault:~# Select Operation: ")

        if choice == '1':
            print("\n--- SINGLE MINT PROTOCOL ---")
            batch_code = input("Enter 3-Letter Batch Code (e.g., ABC): ").strip().upper()
            note_num = input("Enter 4-Digit Note Sequence (e.g., 45): ").strip().zfill(4)
            nonce = str(random.randint(10000, 99999))
            serial = f"{batch_code}{note_num}{nonce}"
            
            if serial in db:
                print("[!] ERROR: Hash collision!")
                continue
                
            amount, note_type, expiry, img_path, area, status = get_common_mint_data()
            
            db[serial] = {
                "amount": int(amount) if amount.isdigit() else amount,
                "type": note_type,
                "expiryDate": expiry,
                "localArea": area,
                "fraudStatus": status,
                "imagePath": img_path
            }
            save_db(db)
            print("\n" + "="*40)
            print(f" MINT SUCCESS! SERIAL TO WRITE:")
            print(f" ---> {serial} <---")
            print("="*40)
            input("\n[SYSTEM PAUSE] Write this exact serial on the physical note. Press ENTER when done...")

        elif choice == '2':
            print("\n--- BULK MINT ASSEMBLY LINE ---")
            batch_code = input("Enter 3-Letter Batch Code (e.g., ABC): ").strip().upper()
            start_num = int(input("Enter STARTING Note Number (e.g., 1): ").strip())
            end_num = int(input("Enter ENDING Note Number (e.g., 50): ").strip())
            
            print("\n[CONFIGURE MASTER PAYLOAD]")
            amount, note_type, expiry, img_path, area, status = get_common_mint_data()
            
            success_count = 0
            generated_serials = []
            
            for i in range(start_num, end_num + 1):
                note_num = str(i).zfill(4)
                nonce = str(random.randint(10000, 99999))
                serial = f"{batch_code}{note_num}{nonce}"
                
                if serial not in db:
                    db[serial] = {
                        "amount": int(amount) if amount.isdigit() else amount,
                        "type": note_type,
                        "expiryDate": expiry,
                        "localArea": area,
                        "fraudStatus": status,
                        "imagePath": img_path
                    }
                    generated_serials.append(serial)
                    success_count += 1
            
            save_db(db)
            print("\n" + "="*40)
            print(f" BULK MINT COMPLETE: {success_count} NOTES")
            print("="*40)
            for s in generated_serials:
                print(f" [ ] {s}")
            print("="*40)
            input("\n[SYSTEM PAUSE] Copy these serials to your physical batch. Press ENTER when finished...")

        elif choice == '3':
            print("\n--- ASSET ROUTING (SINGLE/BULK) ---")
            serials = input("Enter Serial Codes (comma separated): ").strip().split(',')
            new_area = input("Enter New Location / State Bank: ").strip()
            
            count = 0
            for s in serials:
                s = s.strip()
                if s in db:
                    db[s]['localArea'] = new_area
                    count += 1
                else:
                    print(f"[!] 404: {s} Not Found.")
            print(f"[+] ROUTING SUCCESS: {count} assets moved to {new_area}.")
            save_db(db)

        elif choice == '4':
            print("\n--- THREAT STATUS ADJUSTER (SINGLE/BULK) ---")
            serials = input("Enter Serial Codes (comma separated): ").strip().split(',')
            status = select_status()
            
            count = 0
            for s in serials:
                s = s.strip()
                if s in db:
                    db[s]['fraudStatus'] = status
                    count += 1
                else:
                    print(f"[!] 404: {s} Not Found.")
            print(f"[+] SECURITY OVERRIDE: {count} assets updated to '{status}'.")
            save_db(db)

        elif choice == '5':
            print("\n--- MINT CORRECTION QA (Orphan Node Sweeper) ---")
            prefix_map = defaultdict(list)
            for serial in db.keys():
                prefix = serial[:7]
                prefix_map[prefix].append(serial)
            
            collisions_found = False
            for prefix, serial_list in prefix_map.items():
                if len(serial_list) > 1:
                    collisions_found = True
                    print(f"\n[!] COLLISION DETECTED for Physical Note: {prefix}")
                    for idx, s in enumerate(serial_list):
                        print(f"  [{idx + 1}] {s} (Area: {db[s]['localArea']}, Status: {db[s]['fraudStatus']})")
                    
                    keep_idx = input(f"Which one is the REAL physical note? (1-{len(serial_list)}, or 'skip'): ").strip()
                    if keep_idx.isdigit() and 1 <= int(keep_idx) <= len(serial_list):
                        real_serial = serial_list[int(keep_idx) - 1]
                        for s in serial_list:
                            if s != real_serial:
                                del db[s]
                                print(f"[-] PURGED ghost record: {s}")
            
            if not collisions_found:
                print("[+] SYSTEM CLEAN: No physical note collisions detected.")
            else:
                save_db(db)

        elif choice == '6':
            print("\n" + "="*50)
            print("   MACRO-ECONOMIC DASHBOARD v2.0")
            print("="*50)
            
            total_notes = len(db)
            total_value = 0
            
            # Dictionary structure: grouped_data[ForeverStatus][Denomination][BatchCode] = [List of Serials]
            grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
            
            for serial, data in db.items():
                amt = data.get('amount', 0)
                total_value += amt if isinstance(amt, int) else 0
                
                is_forever = "Yes" if "Forever" in data.get('type', '') else "No (Time Limited)"
                batch = serial[:3]
                
                grouped_data[is_forever][amt][batch].append(serial)
            
            print(f"TOTAL CIRCULATING SUPPLY: {total_value} PLC across {total_notes} notes.\n")
            
            for forever_status in sorted(grouped_data.keys(), reverse=True):
                print(f"■ FOREVER STATUS: {forever_status}")
                for amt in sorted(grouped_data[forever_status].keys(), reverse=True):
                    print(f"  ├─ Denomination: {amt} PLC")
                    for batch in sorted(grouped_data[forever_status][amt].keys()):
                        serials = grouped_data[forever_status][amt][batch]
                        print(f"  │  ├─ Batch Group [{batch}]")
                        for s in serials:
                            print(f"  │  │   - {s}")
                        print(f"  │  │  (Total count for {batch}: {len(serials)})")
                print("  │")
                
            input("\n[SYSTEM] Press ENTER to return to the main menu...")

        elif choice == '7':
            print("\n--- MASTER LEDGER DUMP ---")
            print(json.dumps(db, indent=4))
            print("--------------------------")
            input("\n[SYSTEM] Press ENTER to return to the main menu...")

        elif choice == '8':
            serial = input("Enter Serial Code to Modify: ").strip()
            if serial in db:
                print("\n[SYSTEM] Press ENTER to keep current data, or type new data.")
                for key in db[serial].keys():
                    new_val = input(f"Update {key} [{db[serial][key]}]: ").strip()
                    if new_val != "":
                        if key == "amount" and new_val.isdigit():
                            db[serial][key] = int(new_val)
                        else:
                            db[serial][key] = new_val
                print(f"[+] OVERWRITE SUCCESS: {serial} updated.")
                save_db(db)
            else:
                print("[!] ERROR: 404 Serial Not Found.")

        elif choice == '9':
            save_db(db)
            print("Shutting down ERP interface. Goodbye, Lead SysAdmin.")
            break
            
        else:
            print("[!] Invalid command.")

if __name__ == "__main__":
    clear_screen()
    main()
