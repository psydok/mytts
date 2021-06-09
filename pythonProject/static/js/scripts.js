String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
};


function send_form() {
 TEXT_FIELD = document.getElementById("text-input");
  VOICE = document.getElementById("model-select-id");
  SYNTHESIS_RESULT = document.getElementById("table_body_result");

     var data = {
            "text": TEXT_FIELD.value,
            "model": VOICE.value,
        }
 SYNTHESIS_RESULT.innerHTML = "";
fetch("/sinth_temp", {
                method: "post",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
             })
            .then((response) => {
                if (!response.ok) throw response;
                return response.json();
            })
            .then((response) => {
                SYNTHESIS_RESULT.innerHTML = "";
                console.log(response)
                 SYNTHESIS_RESULT.insertAdjacentHTML(
                            "beforeend",
                            TR_PATTERN.format(
                                response["url"],
                                response["speed"]
                            )
                        );
                TEXT_FIELD.readOnly = false;
            })
            .catch((err) => {
                console.log(err);
            });
}

var TR_PATTERN = `
    <tr>
        <td style="width: 100%;">
            <audio controls preload="none">
                <source src="{0}" type="audio/wav">
                Браузер не поддерживается
            </audio>
        </td>
        <td>{1}</td>
    </tr>
`;