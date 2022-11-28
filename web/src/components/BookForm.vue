<template>
  <Transition name="BookForm">
  <div v-if="show" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
            <validation-observer
                ref="observer"
                v-slot="{ invalid }"
              >
                <form @submit.prevent="submit">
                  <validation-provider
                    v-slot="{ errors }"
                    name="Name"
                    rules="required|max:20"
                  >
                  <slot/>
                  <h1>{{ user.id }}</h1>
                    <v-text-field
                      :value=user.id
                      :counter="20"
                      :error-messages="errors"
                      label="Name"
                      required
                    ></v-text-field>
                  </validation-provider>
                  <validation-provider
                    v-slot="{ errors }"
                    name="Page Count"
                  >
                    <v-text-field
                      :value=user.complete
                      :counter="8"
                      :error-messages="errors"
                      :rules="[(v) => (Number(v) > 0 && Number(v) < 1000) || 'Error']"
                      label="Page Count"
                      required
                    ></v-text-field>
                  </validation-provider>
                  <validation-provider
                    v-slot="{ errors }"
                    name="author"
                    rules="required|max:20"
                  >
                    <v-text-field
                      :value=user.title
                      :counter="20"
                      :error-messages="errors"
                      label="Author"
                      required
                    ></v-text-field>
                  </validation-provider>
                  <validation-provider
                    v-slot="{ errors }"
                    name="category"
                    rules="required"
                  >
                    <v-select
                      :value=user.userID
                      :items="items"
                      :error-messages="errors"
                      label="Category"
                      form_data-vv-name="select"
                      required
                    ></v-select>
                  </validation-provider>

                  <v-btn
                    class="mr-4"
                    type="submit"
                    :disabled="invalid"
                  >
                    Add
                  </v-btn>
                  <v-btn
                    class="mr-4"
                    type="submit"
                    :disabled="invalid"
                  >
                    Update
                  </v-btn>
                  <v-btn
                    class="mr-4"
                    type="submit"
                    :disabled="invalid"
                  >
                    Delete
                  </v-btn>
                  <v-btn @click="clear">
                    Clear
                  </v-btn>
                </form>
              </validation-observer>
          <div class="modal-footer">
              <button
                class="modal-default-button"
                @click="$emit('close')"
              >OK</button>
              <button @click="replyDaddy">Reply Parent</button>
          </div>
        </div>
      </div>
    </div>

  </Transition>
</template>


<script>
  import { required, digits, email, max, regex } from 'vee-validate/dist/rules'
  import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'


  setInteractionMode('eager')

  extend('digits', {
    ...digits,
    message: '{_field_} needs to be {length} digits. ({_value_})',
  })

  extend('required', {
    ...required,
    message: '{_field_} can not be empty',
  })

  extend('max', {
    ...max,
    message: '{_field_} may not be greater than {length} characters',
  })

  extend('regex', {
    ...regex,
    message: '{_field_} {_value_} does not match {regex}',
  })

  extend('email', {
    ...email,
    message: 'Email must be valid',
  })

  export default {
  name: 'BookForm',
  props: {
    show: Boolean,
    user: {
        type: Object,
        default: null
    },
  },
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
    myObject: {...this.user},
      author: '',
      name: '',
      pageCount: null,
      select: null,
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
      ],
      checkbox: null,
    }),

    methods: {
      submit () {
        this.$refs.observer.validate()
      },
      clear () {
        this.name = ''
        this.pageCount = ''
        this.author = ''
        this.select = null
        this.checkbox = null
        this.$refs.observer.reset()
      },
      replyDaddy() {
        this.$emit("updateTitle1", "I'm your child");
      },
    },
  }
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 900px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>