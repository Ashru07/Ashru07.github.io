import json
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:
    raise

ROOT = Path(__file__).resolve().parents[1]
pdf_path = ROOT / 'assets' / 'resume.pdf'
out_json = ROOT / 'assets' / 'resume_parsed.json'

def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    texts = []
    for p in reader.pages:
        try:
            texts.append(p.extract_text() or '')
        except Exception:
            texts.append('')
    return '\n'.join(texts)

def find_section(lines, names):
    idx = None
    for i,l in enumerate(lines):
        t = l.strip().upper()
        t_nospace = t.replace(' ', '')
        for n in names:
            ncheck = n.upper().replace(' ', '')
            if n.upper() in t or ncheck in t_nospace:
                idx = i
                break
        if idx is not None:
            break
    if idx is None:
        return ''
    # gather until next all-caps short header (likely a new section) or blank line cluster
    out = []
    for l in lines[idx+1:]:
        if re.match(r'^[A-Z \-]{2,40}$', l.strip()) and l.strip().upper() != l.strip():
            pass
        # stop if we hit another header-like all caps word
        if re.match(r'^[A-Z\s]{2,40}$', l.strip()) and l.strip()==l.strip().upper() and len(l.strip().split())<=6:
            break
        out.append(l)
        if len(out)>30:
            break
    return '\n'.join([o for o in out]).strip()

def extract(data_text: str):
    lines = [l for l in data_text.splitlines()]
    # About: take beginning up to EXPERIENCE or EDUCATION
    about = []
    for l in lines[:60]:
        if re.search(r'EXPERIENCE|EDUCATION|SKILLS|PROJECTS|CERTIFICAT', l.upper()):
            break
        if l.strip():
            about.append(l.strip())
    about_txt = ' '.join(about[:8]).strip()

    education = find_section(lines, ['EDUCATION', 'EDUCATIONAL'])
    certifications = find_section(lines, ['CERTIFICATE', 'CERTIFICATION', 'CERTIFICATES'])

    return {
        'about': about_txt,
        'education': education,
        'certifications': certifications,
        'raw_preview': '\n'.join(lines[:200])
    }

def main():
    if not pdf_path.exists():
        print('ERROR: resume.pdf not found at', pdf_path)
        return
    text = read_pdf(pdf_path)
    parsed = extract(text)

    def clean_spacing(s: str) -> str:
        if not s:
            return s
        # replace sequences of two or more spaces with a marker, remove remaining single spaces (which are between letters),
        # then restore word spaces
        marker = '<<W>>'
        t = re.sub(r' {2,}', marker, s)
        t = t.replace(' ', '')
        t = t.replace(marker, ' ')
        # normalize whitespace
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    parsed['about'] = clean_spacing(parsed.get('about',''))
    parsed['education'] = clean_spacing(parsed.get('education',''))
    parsed['certifications'] = clean_spacing(parsed.get('certifications',''))

    out_json.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding='utf-8')
    print('WROTE', out_json)

if __name__ == '__main__':
    main()
