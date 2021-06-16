from flask_cors import cross_origin
from app import app
from flask import request, jsonify, make_response
from service import SpeechSynthesisService
from base64 import b64encode
from utils.files import out_path


def answer(status, message, audio_bytes: [], filename="", speed="-1", len_text="-1"):
    if str(status).startswith("2"):
        return jsonify(
            status_code=status,
            message=message,
            len_text=len_text,
            speed=speed,
            filename=filename,
            audio_bytes=b64encode(audio_bytes).decode("utf-8")
        )
    else:
        return make_response(jsonify(
            status_code=status,
            message=message
        ), status)


def read_bytes(filename):
    with open(str(out_path) + "/" + filename, "rb") as f:
        audio_bytes = f.read()
    return audio_bytes


@app.route('/synth', methods=['POST'])
@cross_origin()
def synthesize():
    success = "success"
    request_json = request.get_json()
    text = request_json.get("text", "")
    model_type = request_json.get("model_name", "forward_tacotron")
    vocoder_type = request_json.get("vocoder_name", "hifigan")
    if text == "":
        return answer(422, "fail: Bad request. Enter text.", [])
    # if model_type == 'demo-sovaTTS':
    #     return answer(200, success, read_bytes('test_ruslan.wav'), 'test_ruslan.wav', "0", "0")
    try:
        service = SpeechSynthesisService(model_type)
    except ValueError as e:
        service = SpeechSynthesisService('forward_tacotron')
    try:
        response_service = service.generate(text, vocoder=vocoder_type)
    except Exception as e:
        return answer(500, "fail: {0}".format(e), -1, '', "-1", "-1")

    return answer(200, success, read_bytes(response_service['wav_name']),
                  response_service['wav_name'],
                  response_service['speed_synthesis'],
                  response_service['len_text'])


if __name__ == '__main__':
    app.run(debug=True)
