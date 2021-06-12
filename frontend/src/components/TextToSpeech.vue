<template>
  <div class="v-text-to-speech ">
    <div class="card p-3 w-75 justify-content-center">
      <p class="h2 mb-4">Оценить синтез</p>
      <form class="row g-3 needs-validation justify-content-center" novalidate>
        <div class="col-md-4">
          <label for="validationCustom01" class="form-label">Текст для генерации аудио</label>
          <input
              type="text"
              class="form-control"
              id="validationCustom01"
              placeholder="Ваш текст..."
              v-model="text"
              required>
          <div class="valid-feedback">
            Отлично!
          </div>
        </div>
        <div class="col-md-3">
          <label for="validationCustom04" class="form-label">Синтезатор</label>
          <select class="form-select" id="validationCustom04" v-model="model" required>
            <option selected disabled value="">Выберите...</option>
            <option
                v-for="model in this.models"
                :key="model.id"
                :value="model"
                v-text="model.generator"
            />
          </select>
          <div class="invalid-feedback">
            Пожалуйста, выберите модель для синтеза.
          </div>

        </div>
        Для передачи слов-омографов, используйте «+» после ударной гласной: за+мок, замо+к.
        <div class="col-12">
          <button class="btn btn-primary"
                  type="button"
                  v-if="text"
                  :disabled="!!spinner_visible"
                  v-on:click="onSubmit" @click="onReset"
          >Синтезировать
          </button>
        </div>
      </form>

    </div>
    <div class="card p-3 w-75 justify-content-center" v-show="spinner_visible">
      <div class="d-flex align-items-center">
        <strong>Загрузка...</strong>
        <div class="spinner-border ms-auto"
             role="status"
             aria-hidden="true"></div>
      </div>
    </div>

    <div class="card p-3 w-75 justify-content-center" v-show="show_response">
      <div class="col-12 align-items-center">
        <audio id="audio-player"
               controls
               :src="response"
               type="audio/wav"
               style="max-width: 100%;">
          Ваш браузер не поддерживает тег audio!
        </audio>
      </div>
      <div class="col-12" v-if="!is_rate">
        <star-rating class="justify-content-center mb-3"
                     v-model:rating="rating"
                     :show-rating="false"></star-rating>
        <button class="btn btn-primary"
                type="button"
                v-on:click="onSubmitRating"
        >Оценить
        </button>
      </div>
    </div>
    {{ error }}
  </div>
</template>

<script>
import axios from 'axios';
import StarRating from 'vue-star-rating';

export default {
  name: "TextToSpeech",
  components: {
    StarRating
  },
  data() {
    return {
      spinner_visible: false,
      name: '',
      models_id: null,
      vocoder: null,
      model: '',
      models: [{'generator':'demo-sovaTTS', 'id':0},
        {'generator':'forward_tacotron','vocoder':'griffinlim',  'id':0},
        {'generator':'silero', 'id':0},
        {'generator':'fast_speech2', 'id':0}
        ],
      show_response: false,
      response: null,
      error: '',
      is_rate: false,
      rating: 0,
      filename: ''
    }
  },
  mounted() {
    this.$nextTick(function () {// window.location.host'localhost:8060'
      return axios('http://' + 'localhost:8060' + '/api/models', {
        method: "GET",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }
      })
          .then((models) => {
            this.models = models.data;
            return models;
          })
          .catch((error) => console.log(error));
    })
  },
  methods: {
    onSubmitRating(event) {
      event.preventDefault();

      if (!this.rating) return ;
      const data = {
        "filename": this.filename,
        "rate": this.rating
      };
      console.log(data);
      return new Promise((resolve, reject) => {
        axios('http://' +'localhost:8060' + '/api/rating', {
          method: "PUT",
          headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
          },
          data: JSON.stringify(data)
        })
            .then((response) => {
              this.is_rate=true;
              console.log(response.data);
              resolve();
            })
            .catch((error) => {
              console.log(error);
              this.error = error;
              reject(error)

            });
      });
    },
    onSubmit(event) {
      if (this.model && this.text) {
        this.spinner_visible = true;
        const data = {
          "model": this.model.id,
          "model_name": this.model.generator,
          "text": this.text
        };
        event.preventDefault();
        return new Promise((resolve, reject) => {
          axios('http://' + 'localhost:8060' + '/synth', {
            method: "POST",
            headers: {
              'Accept': 'application/json',
              "Content-Type": "application/json",
            },
            data: JSON.stringify(data)
          })
              .then((response) => {
                this.show_response = true;
                this.is_rate=false;
                response=response.data;//JSON.parse(
                console.log(response);
                this.filename = response.filename;
                // this.response = 'http://' + 'localhost:8060' + '/static/wavs/' + this.filename;
                this.spinner_visible = false;
                var q = new Buffer.from(response.audio_bytes, 'base64');

                const blob = new Blob(
                    [new Uint8Array(q)],
                    { type: 'audio/wav' });
                const url = URL.createObjectURL(blob);
                this.response = url;
                const audio = document.getElementById('audio-player');
                audio.load();
                    resolve();
              })
              .catch((error) => {
                console.log(error);
                this.error = error;
                this.spinner_visible = false;
                reject(error)

              });
        });
      }

    },
    onReset(event) {
      event.preventDefault();
      this.spinner_visible = false;
      this.rating = 0;
      this.responses_id = null;
      this.$nextTick(() => {
        this.spinner_visible = true;
      })
    }
  }
}
</script>

<style>


.card {
  margin: 0 auto;
  float: none;
  margin-bottom: 10px;
}
</style>