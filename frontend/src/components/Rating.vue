<template>
  <div class="v-rating">
    <p class="h2 mb-4">Показатели моделей</p>
    <div class="v-rating-info">
      <ul class="list-unstyled">
        <li>Здесь представлены усредненные показатели для каждой модели.</li>
        <li>Показатели отдельной модели пересчитываются на каждую сгенерированную по ней аудиозапись.</li>
        <li>Скорость/символы - это усредненный показатель скорости генерации аудиозаписи моделью на количество переданных ей знаков.</li>
      </ul>
    </div>
    <table class="table">
      <thead>
      <tr>
        <th scope="col">Модель</th>
		<th scope="col">Вокодер</th>
        <th scope="col">Оценка</th>
        <th scope="col">Кол-во оценок</th>
        <th scope="col">Скорость/ символы</th>
      </tr>
      </thead>
      <tbody>
      <v-row-rating
          v-for="model in rating"
          :key="model.id"
          :model_data="model"
      />
      </tbody>
    </table>
  </div>
</template>

<script>
import vRowRating from '../components/RowRating';
import axios from "axios";

export default {
  name: "v-rating",
  components: {
    vRowRating
  },
  data() {
    return {
      rating: []
    }
  },
  mounted() {
    this.$nextTick(function () {//window.location.host'localhost:8060'
      return axios('http://' + 'localhost:8060' + '/api/rating', {
        method: "GET",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }
      })
          .then((rating) => {
            this.rating = rating.data;
            return this.rating;
          })
          .catch((error) => console.log(error));
    })
  }
}
</script>

<style scoped>

</style>