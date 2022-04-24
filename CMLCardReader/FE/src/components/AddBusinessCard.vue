<template>
  <div class="ml-auto">
    <v-dialog width="36rem" v-model="addNewDialog" :persistent="isUploading">
      <v-sheet class="pa-4">
        <h1>Add a business card</h1>
        <v-divider class="my-4" />
        <v-btn
          elevation="0"
          color="#cfcfcf"
          class="w-100 mb-6"
          style="
            aspect-ratio: 3/2 !important;
            width: 100% !important;
            height: unset !important;
            background-size: cover;
            background-position: center;
            transition-property: box-shadow, transform, opacity !important;
          "
          :style="`background-image: url(${imgURL ?? ''})`"
          aria-label="Upload a photo of a business card"
          @click="openImageInput()"
        >
          <v-icon
            x-large
            style="opacity: 0.7"
            :color="imgURL ? 'white' : 'black'"
          >
            mdi-camera-plus
          </v-icon>
        </v-btn>
        <v-btn
          @click="uploadImage()"
          color="primary"
          class="w-100 py-6"
          elevation="0"
        >
          <span v-if="!isUploading">
            <v-icon class="mr-2"> mdi-upload </v-icon> Upload
          </span>
          <span v-else>
            <v-progress-circular indeterminate size="24" width="2" />
          </span>
        </v-btn>
      </v-sheet>
    </v-dialog>
    <v-btn
      color="primary"
      class="ml-auto"
      elevation="0"
      @click="addNewDialog = true"
    >
      <v-icon left>mdi-plus</v-icon> Add new
    </v-btn>

    <input
      @change="setImgFile"
      ref="imgInput"
      type="file"
      accept="image/*"
      class="d-none"
    />
  </div>
</template>

<script>
export default {
  name: "AddBusinessCard",
  data() {
    return {
      addNewDialog: false,
      imgFile: null,
      imgURL: null,
      isUploading: false,
    };
  },
  methods: {
    openImageInput() {
      this.$refs.imgInput.click();
    },
    setImgFile() {
      const file = this.$refs.imgInput.files[0];
      if (!file) return null;
      if (file.size > 1000 * 10_000)
        return alert("Please select a file smaller than 10MB");
      this.imgFile = file;
      //revoke old url
      if (this.imgURL) URL.revokeObjectURL(this.imgURL);
      this.imgURL = URL.createObjectURL(file);
    },
    uploadImage() {
      if (this.isUploading) return null;

      this.isUploading = true;

      //convert image to base64
      const reader = new FileReader();
      reader.readAsDataURL(this.imgFile);
      reader.onload = (e) => {
        const base64 = e.target.result;
        //upload to server
        this.$http
          .post("/business-card", {
            img: base64.replace(/^data:(.*,)?/, ""),
            fileName: this.imgFile.name,
          })
          .then(({ data }) => {
            this.$router.push(`/business-card/${data.id}`);
            this.addNewDialog = false;
          })
          .catch((err) => {
            console.log(err);
          })
          .finally(() => {
            this.isUploading = false;
          });
      };
    },
  },
  watch: {
    addNewDialog() {
      if (this.addNewDialog) {
        this.$refs.imgInput.value = null;
        this.imgFile = null;
        if (this.imgURL) URL.revokeObjectURL(this.imgURL);
        this.imgURL = null;
      }
    },
  },
};
</script>