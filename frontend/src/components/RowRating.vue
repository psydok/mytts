<template>
  <tr>
    <td>{{ model_data.generator }}</td>
	<td>{{ model_data.vocoder }}</td>
    <td>{{ $filters.round(model_data.avg_rate) }}</td>
    <td>{{ $filters.round(model_data.count_rate) }} </td>
    <td>{{ $filters.round(model_data.avg_speed) }} сек на {{ $filters.round(model_data.avg_len_text) }}</td>
  </tr>
</template>

<script>

export default {
  name: "RowRating",
  props: {
    model_data: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {}
  }
}
</script>

<style>

</style>