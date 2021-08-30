<template>
    <div>
        <menuHeader :controlButtons="false"> </menuHeader>
        <b-container fluid>
            <b-row>
                <div class="col-2 full-height bg-dark d-flex flex-column">
                    <div :class="currentImage.id ? 'text-white' : 'text-dark'" class="mb-1">
                        <p> Pasta <b> {{ currentImage.folder_name }} </b> </p>
                        <p>
                            Imagem {{ imageCount }}
                            de {{ currentImage.total_count }}
                        </p>
                    </div>
                    <b-button
                        class="btn btn-warning btn-block my-1"
                        size="sm"
                        @click="$router.push('/folders')">
                        <b-icon-house style="width:20px; height:20px;" class="float-left">
                        </b-icon-house>
                        Página inicial
                    </b-button>
                    <div class="my-2">
                        <template v-for="item in items">
                            <b-button
                                v-if="userPrivileged || item.visible"
                                class="btn btn-block btn-light my-1"
                                size="sm"
                                :key="item.id"
                                @click="addObject(item)">
                                {{ item.description }}
                                <div class="float-right color-display" :style="{'background-color': '#' + item.color}"> </div>
                            </b-button>
                        </template>
                    </div>
                    <b-button
                        class="btn btn-danger btn-block btn-small my-1"
                        size="sm"
                        @click="deleteSelectedObject">
                        Deletar seleção
                    </b-button>
                    <b-button
                        class="btn btn-danger btn-block my-1"
                        size="sm"
                        @click="deleteAllObjects">
                        Deletar tudo
                    </b-button>
                    <b-button 
                        :disabled="!canGetPreviousImage"
                        class="btn btn-warning btn-block my-1"
                        size="sm"
                        @click="getPreviousImage">
                        <b-icon-arrow-left style="width:20px; height:20px;" class="float-left">
                        </b-icon-arrow-left>
                        Refazer anterior
                    </b-button>
                    <b-button
                        v-if="!flagged"
                        class="btn btn-warning btn-block"
                        size="sm"
                        @click="showFlagModal">
                        Sinalizar problema
                    </b-button>
                    <b-button
                        v-if="verifying"
                        class="btn btn-warning btn-block"
                        size="sm"
                        @click="showEndVerificationModal">
                        Concluir verificação
                    </b-button>
                    <b-button
                        v-if="verifying && flagged"
                        class="btn btn-warning btn-block"
                        size="sm"
                        @click="showUnflagModal">
                        Resolver problema
                    </b-button>
                    <b-button
                        v-if="verifying"
                        :disabled="!loaded"
                        class="btn btn-success btn-block align-self-end mt-auto"
                        size="sm"
                        @click="updatePostProcessed">
                        Próxima (sem enviar)
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
                        <div v-if="verifying && flagged">
                            <p class="justify-text m-0 py-0 px-2">
                                <b> Descrição do problema: </b> {{ folder.flag_description }}
                            </p>
                        </div>
                        <imageViewer
                            ref="imageViewer"
                            v-on:updateLoaded="updateLoaded">
                        </imageViewer>
                    </div>
                </div>
            </b-row>
        </b-container>
        <b-modal
            id="flag-modal"
            ok-title="Sinalizar"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="flagFolder">
            <template v-slot:modal-title>
                Sinalizar um problema
            </template>
            <div>
                <p class="justify-text">
                    Sinalize aos administradores um problema com as imagens desta pasta
                    ({{ folder.name }}). Descreva sucintamente o problema encontrado.
                    Note que ao sinalizar um problema com uma pasta, as imagens da mesma
                    não poderão ser classificadas até que um administrador verifique
                    o problema; portanto, ao clicar em 'sinalizar', você será redirecionado
                    à página principal. 
                </p>
                <label for="flagDescription">Descrição do problema: </label>
                <b-form-textarea id="flagDescription" v-model="flagDescription"></b-form-textarea>
            </div>
        </b-modal>
        <b-modal
            id="unflag-modal"
            ok-title="Remover"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="unflagFolder">
            <template v-slot:modal-title>
                Remover sinalização de problema
            </template>
            <div>
                <p class="justify-text">
                    Deseja remover a sinalização do problema (descrito abaixo) desta pasta?
                    Note que ao fazer isso, esta pasta será novamente disponibilizada
                    para classificação.
                </p>
                <p class="justify-text">
                    <b> Descrição do problema: </b> {{ folder.flag_description }}
                </p>
            </div>
        </b-modal>
        <b-modal
            id="end-verification-modal"
            ok-title="Concluir"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="endVerification">
            <template v-slot:modal-title>
                Concluir verificação
            </template>
            <div>
                <p class="justify-text">
                    Concluir a verificação desta pasta implica em remover o progresso
                    de verificação das pastas, isto é, da próxima vez que você decidir
                    visualizar as imagens desta pasta, a exibição terá início na
                    primeira imagem. Adicionalmente, você pode optar por marcar essa
                    pasta como verificada, mesmo não tendo visualizado todas as imagens.
                    Deseja continuar?
                </p>
                <b-form-checkbox
                    v-model="setVerifiedWhenDone"
                    style="padding-left:32px;">
                    Marcar esta pasta como verificada
                </b-form-checkbox>
            </div>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';
import { BIconHouse, BIconArrowLeft } from 'bootstrap-vue';
import menuHeader from './shared/Header.vue'
import imageViewer from './classifier/ImageViewer.vue'

export default {
    name: 'classifier',
    components: {
        menuHeader,
        imageViewer,
        BIconHouse,
        BIconArrowLeft,
    },
    props: ['folder', 'verifying'],
    data() {
        return {
            items: [],
            currentImage: {
                id: null,
                data: null,
                folder_id: null,
                folder_name: null,
                processed_count: null,
                post_processed_count: null,
                total_count: null,
            },
            loaded: false,
            flagDescription: '',
            setVerifiedWhenDone: false,
            flagged: false,
            userPrivileged: false,
        }
    },
    computed: {
        imageCount() {
            return 1 + (this.verifying ? 
                this.currentImage.post_processed_count - this.currentImage.post_processed:
                this.currentImage.processed_count - this.currentImage.processed);
        },
        canGetPreviousImage() {
            return this.loaded && this.imageCount > 1;
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
            this.flagged = this.folder.flagged;
            this.getNextImage();
        });
    },
    created() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.items = [];
            this.userPrivileged = this.$session.get('user_privileged');
            axios.get(this.backend + '/items').then(res => {
                if (res.data) res.data.items.forEach((el) => this.items.push(el));
            }).catch((err) => console.log(err));
        },
        updateImage() {
            this.$refs.imageViewer.updateImage(this.currentImage, this.items);
        },
        addObject(item) {
            this.$refs.imageViewer.addObject(item);
        },
        deleteSelectedObject() {
            this.$refs.imageViewer.deleteSelectedObject();
        },
        deleteAllObjects() {
            this.$refs.imageViewer.deleteAllObjects();
        },
        updateLoaded(value) {
            this.loaded = value;
        },
        postLabels() {
            this.loaded = false;
            const labels = this.$refs.imageViewer.getLabels(this.items);
            axios.post(this.backend + '/images', {
                'image_id': this.currentImage.id,
                'labels': labels,
            }).then(res => {
                console.log(res);
                if (this.verifying) {
                    this.updatePostProcessed();
                } else {
                    this.getNextImage();                    
                }
            }).catch(err => console.log(err));
        },
        updatePostProcessed() {
            this.loaded = false;
            axios.put(this.backend + '/images/post_processed', {
                'image_id': this.currentImage.id,
            }).then(res => {
                console.log(res);
                this.getNextImage();
            }).catch(err => console.log(err));
        },
        getNextImage() {
            this.loaded = false;
            axios.get(this.backend + '/images/next', {
                params: {
                    folder_id: this.folder.id,
                    post_processing: this.verifying,
                },
            }).then(res => {
                console.log(res);
                if (res.data.data) {
                    this.currentImage = {...res.data};
                    this.updateImage();
                } else if (this.verifying) {
                    axios.put(this.backend + '/images/clear', {
                        'folder_id': this.folder.id,
                        'verified' : true,
                    }).then(res => {
                        console.log(res);
                        this.$router.push('/folders');
                    }).catch(err => console.log(err));
                } else if (this.currentImage.total_count - this.currentImage.processed_count <= 1) {
                    axios.put(this.backend + '/folders/processed', {
                        'folder_id': this.folder.id,
                        'processed': true,
                    }).then(res => {
                        console.log(res);
                        this.$router.push('/folders');
                    }).catch(err => console.log(err));
                } else {
                    this.flagDescription = "Erro ao buscar nova imagem (PROBLEMA DETECTADO AUTOMATICAMENTE)."
                    this.flagFolder();
                }
            }).catch(err => console.log(err));
        },
        getPreviousImage() {
            this.loaded = false;
            axios.get(this.backend + '/images/previous', {
                params: {
                    folder_id: this.folder.id,
                    post_processing: this.verifying,
                    image_id: this.currentImage.id,
                }
            }).then(res => {
                console.log(res);
                if (res.data.data) {
                    this.currentImage = {...res.data};
                    this.updateImage();
                }
            }).catch(err => console.log(err));
        },
        showFlagModal() {
            this.$bvModal.show('flag-modal');
        },
        flagFolder() {
            axios.put(this.backend + '/folders/flag', {
                folder_id: this.folder.id,
                flag_description: this.flagDescription,
            }).then(res => {
                console.log(res);
                this.$router.push('/folders');
            }).catch(err => console.log(err));
        },
        showUnflagModal() {
            this.$bvModal.show('unflag-modal');
        },
        unflagFolder() {
            axios.put(this.backend + '/folders/unflag', {
                folder_id: this.folder.id
            }).then(res => {
                console.log(res);
                this.$router.push('/folders');
            }).catch(err => console.log(err));
        },
        showEndVerificationModal() {
            this.$bvModal.show('end-verification-modal');
        },
        endVerification() {
            axios.put(this.backend + '/images/clear', {
                'folder_id': this.folder.id,
                'verified' : this.folder.verified || this.setVerifiedWhenDone,
            }).then(res => {
                console.log(res);
                this.$router.push('/folders');
            }).catch(err => console.log(err));
        },
    },
}
</script>

<style scoped>

.full-height {
    min-height: 100%;
    min-height: 93vh;
    height: 100%;
}

.color-display {
    width: 20px;
    height: 20px;
    border: 2px solid #000000;
}

.justify-text {
    text-align: justify;
    text-justify: inter-word;
    word-wrap: break-word;
}

</style>
