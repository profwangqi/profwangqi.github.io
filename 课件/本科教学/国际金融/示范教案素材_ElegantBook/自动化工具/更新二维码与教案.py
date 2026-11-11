from pathlib import Path
import json,shutil,subprocess,argparse
ROOT=Path(__file__).resolve().parent.parent;B=ROOT/'教案源码'
Q=B/'assets/qrcodes'
def main(compile_pdf=False):
 import qrcode
 from qrcode.image.svg import SvgPathImage
 data=json.loads((ROOT/'GitHub二维码链接.json').read_text());base=data['base_url']
 macros={'top':'CourseEntryURL','risk-lab':'RiskLabURL','s5':'AIReviewURL','s6':'QuizTransferURL'}
 tex=['% 已按公开GitHub Pages链接配置。','\\newcommand{\\PublicBaseURL}{'+base.replace('%',r'\%')+'}']
 for item in data['qr']:
  url=base+'#'+item['anchor'];q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=20,border=4);q.add_data(url);q.make(fit=True)
  p=Q/item['file'];q.make_image(fill_color='#173754',back_color='white').save(p);q.make_image(image_factory=SvgPathImage).save(p.with_suffix('.svg'))
  tex.append('\\newcommand{\\'+macros[item['anchor']]+'}{'+url.replace('%',r'\%').replace('#',r'\#')+'}')
 (B/'二维码配置_ElegantBook.tex').write_text('\n'.join(tex)+'\n')
 if compile_pdf:
  engine=shutil.which('xelatex')
  if not engine:raise SystemExit('二维码已更新。重新编译PDF需要安装TeX Live或MacTeX。')
  (B/'_build').mkdir(exist_ok=True)
  for _ in range(2):subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-output-directory=_build','国际金融_示范教案_ElegantBook.tex'],cwd=B,check=True)
  shutil.copy2(B/'_build/国际金融_示范教案_ElegantBook.pdf',B/'国际金融_示范教案_ElegantBook.pdf');shutil.copy2(B/'_build/国际金融_示范教案_ElegantBook.pdf',ROOT.parent/'国际金融_示范教案_ElegantBook.pdf')
 print('二维码配置已更新。源码和PDF改动后需再同步至GitHub Pages仓库。')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--compile',action='store_true');args=ap.parse_args();main(args.compile)
