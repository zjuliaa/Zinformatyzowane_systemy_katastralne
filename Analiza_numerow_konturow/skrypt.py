import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def podziel(name) -> list:
    return name.split("-") if "-" in name else [name] 

def usun(name, skip):
    while name and any(name.startswith(letter) for letter in skip):
        for letter in skip:
            if name.startswith(letter):
                name = name[len(letter):] 
                break  
    return name  

def print_results(title, items, output_widget):
    output_widget.insert(tk.END, f"{title}: {len(items)}\n")
    if items:
        for index, item in enumerate(items, start=1):
            output_widget.insert(tk.END, f"  {index}. {item}\n")
    output_widget.insert(tk.END, "\n")

def wczytaj_plik():
    file_path = filedialog.askopenfilename(
        title="Wybierz plik", 
        filetypes=[("Text files", "*.txt")]
    )
    if not file_path:
        return
    path_entry.delete(0, tk.END)
    path_entry.insert(0, file_path)

    try:
        with open(file_path, 'r', encoding='latin2') as plik:
            dzialka = [linia.strip() for linia in plik if 3 < len(linia.strip()) < 20]

        OFU = ["B","Ba","Bi","Bp","Bz","K","dr","Tk","Ti","Tp","Wm","Wp","Ws","Tr","Ls","Lz","N"]
        OFU1 = ["S", "Br", "Wsr", "W", "Lzr"]
        OFU2 = ["R", "S", "Br", "Wsr", "W", "Lzr"]
        OFU3 = ["Ł", "S", "Br", "Wsr", "W", "Lzr"]
        OFU4 = ["Ps", "S", "Br", "Wsr", "W", "Lzr"]
        OFU5 = ["Ls", "W"]
        OFU6 = ["R", "S", "Ł", "Ps", "Br", "Wsr", "W", "Lzr", "Ls", "Lz"]
        OZU = ["Ł", "Ps", "Ls", "Lz"]
        OZU1 = ["R"]
        OZU2 = ["Ł"]
        OZU3 = ["Ps"]
        OZU4 = ["Lz"]
        OZK = ["I", "II", "III", "IV", "V", "VI"]
        OZK1 = ["I", "II", "IIIa", "IIIb", "IVa", "IVb", "V", "VI", "VIz"]
        x =["ü"]

        prawidlowe, ukosniki, zapis_numeru, oznaczenie_ofu, spacja, bledne, duplikaty, brak_ozk, nieprawidlowe_ozk, do_usuniecia, do_usuniecia1, do_usuniecia2 = [], [], [], [], [], [], [], [], [], [], [], []
        dzialki_dict = {}

        for nazwa in dzialka:
            if nazwa.count("/") != 1:
                ukosniki.append(nazwa)
            elif " " in nazwa:
                spacja.append(nazwa)
                pass
            else:
                part0, separator, part1 = nazwa.partition("/")                    
                valid_number = True
                for znak in part0:
                    if not (znak.isnumeric() or znak == "-"):
                        zapis_numeru.append(nazwa)
                        valid_number = False
                        break
                if valid_number: 
                    name = podziel(part1)
                    if part0 in dzialki_dict:
                        if dzialki_dict[part0] != part1:
                            duplikaty.append(nazwa)
                            continue  
                    else:
                        dzialki_dict[part0] = part1
                    if name[0] in OFU:
                        if len(name) == 1:
                            prawidlowe.append(nazwa) 
                            found = True
                        else:
                            bledne.append(nazwa)  
                            found = True
                    else:
                        for element in name:
                            if element == "E":
                                oznaczenie_ofu.append(nazwa)
                                found = True  
                                break 
                            if len(name) == 1:
                                if element in OFU:
                                    prawidlowe.append(nazwa)
                                    found = True
                                else:
                                    found = False
                                    for typ_gruntu in OZU:
                                        if element.startswith(typ_gruntu):
                                            klasa = element[len(typ_gruntu):]  
                                            if klasa in OZK:
                                                prawidlowe.append(nazwa)
                                                found = True
                                                break  
                                    if not found:  
                                        for typ_gruntu1 in OZU1:  
                                            if element.startswith(typ_gruntu1):
                                                klasa = element[len(typ_gruntu1):]  
                                                if klasa in OZK1:
                                                    prawidlowe.append(nazwa)
                                                    found = True
                                                    break                                  
                                break
                            if name[0] in OFU2:
                                for typ_gruntu in OZU1:
                                    if element.startswith(typ_gruntu):
                                        klasa = element[len(typ_gruntu):]  
                                        if klasa in OZK1:
                                            prawidlowe.append(nazwa)
                                            found = True
                                            break  
                            if not found and name[0] in OFU3:
                                for typ_gruntu in OZU2:
                                    if element.startswith(typ_gruntu):
                                        klasa = element[len(typ_gruntu):]  
                                        if klasa in OZK:
                                            prawidlowe.append(nazwa)
                                            found = True
                                            break
                            if not found and name[0] in OFU4:
                                for typ_gruntu in OZU3:
                                    if element.startswith(typ_gruntu):
                                        klasa = element[len(typ_gruntu):]  
                                        if klasa in OZK:
                                            prawidlowe.append(nazwa)
                                            found = True
                                            break
                            if not found and name[0] in OFU5:
                                for typ_gruntu in OZU4:
                                    if element.startswith(typ_gruntu):
                                        klasa = element[len(typ_gruntu):]  
                                        if klasa in OZK:
                                            prawidlowe.append(nazwa)
                                            found = True
                                            break
                    if not found:
                        bledne.append(nazwa)
        output_text.delete("1.0", tk.END)

        for blad in bledne:
            part0, separator, part1 = blad.partition("/")  
            name = podziel(part1)  
            if name:  
                first_part = name[0]  
                for ofu_element in x:
                    if first_part.startswith(ofu_element) or first_part in OFU:  
                        oznaczenie_ofu.append(blad)
                        do_usuniecia.append(blad)  
                        break  
        for blad in do_usuniecia:
            bledne.remove(blad)
        
        for blad in bledne:
            part0, separator, part1 = blad.partition("/")  
            name = podziel(part1)  
            if len(name) == 1 and name[0] in OFU6:
                brak_ozk.append(blad)  
                do_usuniecia1.append(blad)
        
        for blad in do_usuniecia1:
            bledne.remove(blad)

        for blad in bledne:
            part0, separator, part1 = blad.partition("/") 
            name = podziel(part1) 
            if name: 
                for ozu in OZU + OZU1:
                    if name[0].startswith(ozu):  
                        ozk = name[0][len(ozu):]                          
                        if ozk:  
                            if (ozu in OZU and ozk not in OZK) or (ozu in OZU1 and ozk not in OZK1):
                                nieprawidlowe_ozk.append(blad)  
                                do_usuniecia2.append(blad)
        
        for blad in do_usuniecia2:
            bledne.remove(blad)

        bledy = ukosniki + zapis_numeru + oznaczenie_ofu + spacja + bledne + duplikaty + brak_ozk + nieprawidlowe_ozk
        liczba_bledow_entry.delete(0, tk.END)
        liczba_bledow_entry.insert(0, str(len(bledy)))
        if len(ukosniki) != 0:
            print_results("Nieprawidłowa liczba ukośników", ukosniki, output_text)
        if len(zapis_numeru) != 0:
            print_results("Niewłaściwy zapis", zapis_numeru, output_text)
        if len(oznaczenie_ofu) != 0:
            print_results("Nieprawidłowe oznaczeniem OFU", oznaczenie_ofu, output_text)
        if len(brak_ozk) != 0:
            print_results("Brak oznaczenia OZU", brak_ozk, output_text)
        if len(nieprawidlowe_ozk) != 0:
            print_results("Nieprawidłowe oznaczeniem OZK", nieprawidlowe_ozk, output_text)
        if len(bledne) != 0:
            print_results("Nieprawidłowe oznaczeniem OZU", bledne, output_text)
        if len(spacja) != 0:
            print_results("Nieprawidłowa liczba spacji", spacja, output_text)
        if len(duplikaty) != 0:
            print_results("Duplikat", duplikaty, output_text)
        if len(prawidlowe) != 0:
            print_results("Prawidłowe numery konturów", prawidlowe, output_text)

    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem: {e}")

def zapisz_wyniki():
    file_path = filedialog.asksaveasfilename(
        title="Zapisz plik",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not file_path:
        return
    
    with open(file_path, 'w', encoding='latin2') as plik:
        plik.write(output_text.get("1.0", tk.END))

root = tk.Tk()
root.title("Analiza numerów działek")
root.geometry("600x500")
path_entry = tk.Entry(root, width=57)
path_entry.place(x=10, y=10)
wczytaj_btn = tk.Button(root, text="Wczytaj plik i wyszukaj błędy", command=wczytaj_plik)
wczytaj_btn.place(x=10, y=40)
zapisz_btn = tk.Button(root, text="Zapisz wyniki", command=zapisz_wyniki)
zapisz_btn.place(x=200, y=40)
zamknij_btn = tk.Button(root, text="Zamknij", command=root.quit)
zamknij_btn.place(x=300, y=40)
liczba_bledow_label = tk.Label(root, text="Liczba błędów:", font=("Arial", 12))
liczba_bledow_label.pack(pady=5, side=tk.LEFT)
liczba_bledow_entry = tk.Entry(root, width=10, font=("Arial", 12))
liczba_bledow_entry.pack(pady=5, side=tk.LEFT)
liczba_bledow_entry.insert(0, "0")
output_text = ScrolledText(root, wrap=tk.WORD, height=20)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=80)
root.mainloop()
