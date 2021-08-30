<template>
    <div>
        <menuHeader :controlButtons="false"> </menuHeader>
        <b-container fluid>
            <b-row>
                <div class="col-2 full-height bg-dark d-flex flex-column">
                    <div :class="currentImage.id ? 'text-white' : 'text-dark'" class="mb-1">
                        <p> Pasta <b> {{ currentImage.folder_name }} </b> </p>
                    </div>
                    <b-button
                        class="btn btn-block btn-light my-1"
                        size="sm"
                        @click="addObject">
                        Adicionar Régua
                        <div class="float-right color-display" :style="{'background-color': '#FF0000'}"> </div>
                    </b-button>
                    <b-button
                        class="btn btn-danger btn-block my-1"
                        size="sm"
                        @click="deleteAllObjects">
                        Deletar
                    </b-button>
                    <b-button
                        :disabled="!loaded"
                        class="btn btn-success btn-block align-self-end mb-3"
                        size="sm"
                        :class="verifying ? '' : 'mt-auto'"
                        @click="postLabels">
                        Enviar
                    </b-button>
                </div>

                <div class="col-10 full-height px-0 py-0">
                    <template v-if="!loaded">
                        <div class="d-flex justify-content-center my-5">
                            <b-spinner label="Loading..."></b-spinner>
                        </div>
                    </template>
                    <div v-show="loaded">
                        <div v-if="verifying">
                            <p class="justify-text m-0 py-0 px-2">
                                <b> Descrição do problema: </b> {{ folder.flag_description }}
                            </p>
                        </div>
                        <rulerImageViewer
                            ref="rImageViewer"
                            v-on:updateLoaded="updateLoaded">
                        </rulerImageViewer>
                    </div>
                </div>
            </b-row>
        </b-container>
    </div>
</template>


<script>
import axios from 'axios';
import menuHeader from './shared/Header.vue'
import rulerImageViewer from './classifier/RulerImageViewer.vue'

export default {
    name: 'ruler',
    components: {
        menuHeader,
        rulerImageViewer,
    },
    props: ['folder', 'verifying', 'currentImage'],
    data() {
        return {
            loaded: false,
            items: [],
        }
    },
    beforeCreate() {
        if (!this.$session.exists()) this.$router.push('/login');
    },
    mounted() {
        this.$nextTick(() => {
            if (!this.folder) {
                this.$router.push('/folders')
                return;
            }
        });
        console.log("mounted");
        this.updateImage()
    },
    created() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.items = [];
            axios.get(this.backend + '/items').then(res => {
                if (res.data) res.data.items.forEach((el) => this.items.push(el));
            }).catch((err) => console.log(err));
            console.log("refresh")
        },
        updateImage() {
            console.log("updateImage");
            this.$refs.rulerImageViewer.updateImage(this.currentImage);
        },
        addObject() {
            this.$refs.rulerImageViewer.addObject();
        },
        deleteAllObjects() {
            this.$refs.rulerImageViewer.deleteAllObjects();
        },
        updateLoaded(value) {
            console.log(value);
            this.loaded = value;
        },
        postLabels() {
            this.loaded = false;
            const labels = this.$refs.rulerImageViewer.getLabels(this.items);
            axios.post(this.backend + '/images', {
                'image_id': this.currentImage.id,
                'labels': labels,
            }).then(res => {
                console.log(res);
            }).catch(err => console.log(err));
        },
    }
}
</script>