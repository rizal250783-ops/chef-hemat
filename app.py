import os
import time
from google import genai
from google.genai import types

# ---------- Konfigurasi (parameter kreatif) ----------
SYSTEM_PROMPT = """Kamu adalah 'Chef Hemat', asisten resep untuk anak kos.
Gaya bahasa: santai dan lucu, pakai bahasa Indonesia sehari-hari.
Tugas: user menyebut bahan yang ada, kamu beri 1 ide resep murah dan mudah.
Format jawaban: nama masakan, bahan tambahan (jika perlu), dan langkah singkat (maksimal 5 langkah).
Jika pertanyaan di luar urusan masak, tolak dengan candaan lalu ajak balik ke topik masak."""

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# chat session = memory: bot ingat percakapan sebelumnya
chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.8,
    ),
)

print("=== Chef Hemat - Asisten Resep Anak Kos ===")
print("Ketik bahan yang kamu punya. Ketik 'keluar' untuk berhenti.\n")

while True:
    user = input("Kamu: ")
    if user.lower() == "keluar":
        print("Chef Hemat: Sampai jumpa, jangan lupa cuci piring ya!")
        break
    # Coba sampai 4 kali jika server Gemini sedang sibuk (error 503)
    for percobaan in range(4):
        try:
            jawaban = chat.send_message(user)
            print("\nChef Hemat:", jawaban.text, "\n")
            break
        except Exception as e:
            if percobaan == 3:
                print("\nChef Hemat: Server sedang sibuk, coba lagi nanti ya.", "\n")
            else:
                print("(server sibuk, mencoba lagi...)")
                time.sleep(5)
