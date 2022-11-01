from config import DEBUG, IMAGE_PATH
from app_logger import logger_output
import qrcode
from pathlib import Path

qr_dir = Path(IMAGE_PATH)
qr_dir.mkdir(parents=True, exist_ok=True)


def make_qr(qr_text, user_id):
    qr_full_name = ''
    try:
        qr_file_name = f'{user_id}.png'
        qr_full_name = qr_dir / qr_file_name
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_H,
                           box_size=24,
                           border=2)
        qr.add_data(qr_text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color='black', back_color='white')
        qr_img.save(qr_full_name)
        return 'success'
    except Exception as err:
        logger_output(f'QR code generation error: {str(err)}', DEBUG, 'error')
        return 'error'
