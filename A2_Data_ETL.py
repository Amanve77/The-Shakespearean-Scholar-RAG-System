import pdfplumber
import re
import json
from pathlib import Path

SCENE_DESCRIPTIONS = {
    (1, 1): "Street of Rome - Citizens celebrate Caesar's triumph",
    (1, 2): "A public place - Cassius begins manipulating Brutus",
    (1, 3): "A street at night - Omens disturb Rome",
    (2, 1): "Brutus's house - Brutus decides on conspiracy",
    (2, 2): "Caesar's house - Caesar and Calpurnia discuss omens",
    (2, 3): "A street - Artemidorus prepares warning",
    (2, 4): "Another part of Rome - Portia anxiously awaits news",
    (3, 1): "The Capitol - Caesar is assassinated",
    (3, 2): "The Forum - Brutus and Antony deliver funeral orations",
    (3, 3): "A street - Mob violence begins",
    (4, 1): "House of Antony - The triumvirate plans revenge",
    (4, 2): "Brutus's camp - Argument",
    (4, 3): "Brutus's tent - Ghosts and battle prep",
    (5, 1): "Plains near Philippi - Armies prepare for battle",
    (5, 2): "The battlefield - Fighting begins",
    (5, 3): "Another part of the field - Casualties mount",
    (5, 4): "The battlefield - Brutus falls",
    (5, 5): "The battlefield - Aftermath and conclusion"
}
SOLILOQUIES = {(2, 1): ["BRUTUS"], (3, 2): ["ANTONY"]}
CHARACTER_TYPES = {"BRUTUS": "protagonist", "ANTONY": "protagonist", "CASSIUS": "antagonist"}

def roman_to_int(roman):
    val_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_val = 0
    for char in reversed(roman.upper()):
        val = val_map.get(char, 0)
        if val < prev_val: total -= val
        else: total += val
        prev_val = val
    return total

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [p.extract_text() for p in pdf.pages if p.extract_text()]
    return "\n".join(pages)

def clean_and_find_play_start(raw_text):
    txt = re.sub(r'FTLN\s*\d+', '', raw_text)
    txt = re.sub(r'Page\s*\d+', '', txt)
    txt = re.sub(r'\n{2,}', '\n', txt)
    match = re.search(r"(ACT\s*1[\s\.]*(SCENE|SC)?\.?\s*1)", txt, re.IGNORECASE)
    if match:
        txt = txt[match.start():]
    return txt

def chunk_play_folger(txt, scene_desc_map, soliloquies_map, char_types):
    lines = txt.split('\n')
    chunks = []
    act, scene = None, None
    scene_desc = ""
    curr_speaker, curr_lines = None, []
    chunk_id = 0

    for l in lines:
        l = l.strip()
        match_act = re.match(r"^ACT\s*([IVX\d]+)\s*$", l, re.IGNORECASE)
        if match_act:
            act = int(match_act.group(1)) if match_act.group(1).isdigit() else roman_to_int(match_act.group(1))
            scene = None
            continue

        if re.match(r"^(?:ACT\s*[IVX\d]+\s*)?SCENE\s+([IVX\d]+)\s*$", l, re.IGNORECASE) or \
           re.match(r"^(?:ACT\s*[IVX\d]+\s*)?SC\.\s*([IVX\d]+)\s*$", l, re.IGNORECASE):
            scene_num_str = re.findall(r"[IVX\d]+", l)[-1]
            scene = int(scene_num_str) if scene_num_str.isdigit() else roman_to_int(scene_num_str)
            scene_desc = scene_desc_map.get((act, scene), f"Act {act}, Scene {scene}")
            continue

        if re.match(r"^[A-Z][A-Z\s\-]+$", l) and len(l) > 2:
            if curr_speaker and curr_lines:
                chunk_id += 1
                is_soliloquy = ((act, scene) in soliloquies_map and curr_speaker in soliloquies_map[(act, scene)])
                char_type = char_types.get(curr_speaker, "minor")
                text = "\n".join(curr_lines).strip()
                if text:
                    chunks.append({
                        "chunk_id": f"C{chunk_id:04d}",
                        "text": text,
                        "act": act,
                        "scene": scene,
                        "speaker": curr_speaker,
                        "scene_description": scene_desc,
                        "is_soliloquy": is_soliloquy,
                        "character_type": char_type,
                        "lines": len(text.split('.'))
                    })
            curr_speaker = l
            curr_lines = []
            continue

        if l:
            curr_lines.append(l)

    if curr_speaker and curr_lines:
        chunk_id += 1
        is_soliloquy = ((act, scene) in soliloquies_map and curr_speaker in soliloquies_map[(act, scene)])
        char_type = char_types.get(curr_speaker, "minor")
        text = "\n".join(curr_lines).strip()
        if text:
            chunks.append({
                "chunk_id": f"C{chunk_id:04d}",
                "text": text,
                "act": act,
                "scene": scene,
                "speaker": curr_speaker,
                "scene_description": scene_desc,
                "is_soliloquy": is_soliloquy,
                "character_type": char_type,
                "lines": len(text.split('.'))
            })

    return chunks

def main():
    script_dir = Path(__file__).parent
    pdf_path = script_dir / "julius-caesar.pdf"
    if not pdf_path.is_file():
        print("❌ File 'julius-caesar.pdf' not found.")
        return

    print("Extracting raw text...")
    raw_text = extract_text(pdf_path)
    print("Cleaning and finding start of play...")
    cleaned_text = clean_and_find_play_start(raw_text)
    print("Chunking play by act/scene/speaker...")
    chunks = chunk_play_folger(cleaned_text, SCENE_DESCRIPTIONS, SOLILOQUIES, CHARACTER_TYPES)

    out_file = "processed_chunks.jsonl"
    with open(out_file, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + '\n')
    print(f"✓ Saved {len(chunks)} chunks to '{out_file}'")
    if chunks:
        print("Sample chunks:")
        print(json.dumps(chunks[0], indent=2))
        print(json.dumps(chunks[-1], indent=2))

if __name__ == "__main__":
    main()

