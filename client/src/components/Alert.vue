<template>
  <div>
    <b-alert dismissible variant="success" :show="dismissCountDown"
    @dismissed="dismissCountDown=0">{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
  data() {
    return {
      dismissCountDown: 5,
    };
  },
  mounted() {
  },
};
</script>
