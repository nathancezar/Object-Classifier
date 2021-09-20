<template>
    <div>
        <b-navbar class="header navbar navbar-dark bg-dark text-white" toggleable="lg">
            <b-navbar-brand><b>Object Classifier</b></b-navbar-brand>
            <b-navbar-nav class="ml-auto">
                <span><b>Usuário:</b> {{this.$session.get('user_name')}} </span>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="showExportByTypeModal">
                    Exportar por tipo
                </b-button>
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="exportAll">
                    Exportar tudo
                </b-button>
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="insertDatabase">
                    Inserir no banco
                </b-button>
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="showTrainModal">
                    Treinar
                </b-button>
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="showLogModal">
                    Ver logs
                </b-button>
                <b-button
                    v-if="controlButtons && this.$session.exists() && userPrivileged"
                    class="btn btn-warning mx-1"
                    size="sm"
                    @click="showInsertFaqModal">
                    Inserir FAQ
                </b-button>
                <b-button
                    v-if="this.$session.exists()"
                    class="btn btn-info mx-1"
                    size="sm"
                    @click="showFaqModal">
                    FAQ
                </b-button>
                <b-button
                    v-if="this.$session.exists()"
                    class="btn btn-danger ml-1"
                    size="sm"
                    @click="doLogout">
                    Logout
                </b-button>
            </b-navbar-nav>
        </b-navbar>

        <b-modal
            id="train-modal"
            ok-title="Treinar"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="train">
            <template v-slot:modal-title>
                Treinar a rede neural
            </template>
            <b-row class="my-1">
                <b-col class="my-1" sm="3"> <label for="dataset">Dataset</label> </b-col>
                <b-col class="my-1" sm="9">
                    <b-form-input id="dataset" v-model="training.dataset"></b-form-input>
                </b-col>
                <b-col class="my-1" sm="3"> <label for="nclasses">Nº classes</label> </b-col>
                <b-col class="my-1" sm="9">
                    <b-form-input id="nclasses" v-model="training.nclasses"></b-form-input>
                </b-col>
                <b-col class="my-1" sm="3"> <label for="epochs">Epochs</label> </b-col>
                <b-col class="my-1" sm="9">
                    <b-form-input id="epochs" v-model="training.epochs"></b-form-input>
                </b-col>
                <b-col class="my-1" sm="3"> <label for="batch_size">Batch size</label> </b-col>
                <b-col class="my-1" sm="9">
                    <b-form-input id="batch_size" v-model="training.batch_size"></b-form-input>
                </b-col>
                <b-col class="my-1" sm="3"> <label for="batch_size">Dispositivo</label> </b-col>
                <b-col class="my-1" sm="9">
                    <b-form-group>
                        <b-form-radio-group v-model="training.device">
                            <b-form-radio value="cpu"> CPU </b-form-radio>
                            <b-form-radio value="cuda"> CUDA </b-form-radio>
                        </b-form-radio-group>
                    </b-form-group>
                </b-col>
            </b-row>
        </b-modal>

        <b-modal
            id="log-modal"
            :hide-footer="true"
            size="xl">

            <template v-slot:modal-title>
                Logs de treinamento
            </template>
            <b-table
                :items=logs
                :fields=logFields
                head-variant="dark"
                striped>
                <template v-slot:cell(file)="data">
                    <b> {{ data.value }} </b>
                    <b-button
                        class="btn btn-info float-right"
                        @click="data.toggleDetails">
                        Detalhes
                    </b-button>
                </template>

                <template v-slot:row-details="row">
                    <span style="white-space:pre-wrap;"> {{ row.item.text }} </span>
                </template>
            </b-table>
        </b-modal>

        <b-modal
            id="faq-modal"
            :hide-footer="true"
            size="xl">
            <template v-slot:modal-title>
                FAQ
            </template>
            <div>
                <template v-if="faqs.length">
                    <div v-for="faq in faqs" :key="faq.id" class="my-3 p-2 simple-border justify-text">
                        <h5> <b> Q: {{ faq.question }} </b> </h5>
                        <h5> R: {{ faq.answer }} </h5>
                    </div>
                </template>
                <template v-else>
                    Nenhum FAQ registrado.
                </template>
            </div>
        </b-modal>

        <b-modal
            id="insert-faq-modal"
            ok-title="Inserir"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="insertFaq">
            <template v-slot:modal-title>
                Inserir FAQ
            </template>
            <div>
                <label for="question">Pergunta</label>
                <b-form-textarea id="question" v-model="faq.question"></b-form-textarea>
                <label for="answer">Resposta</label>
                <b-form-textarea id="answer" v-model="faq.answer"></b-form-textarea>
            </div>
        </b-modal>

        <b-modal
            id="export-by-type-modal"
            ok-title="Exportar por tipo"
            ok-variant="warning"
            cancel-title="Cancelar"
            @ok="exportByType">
            <template v-slot:modal-title>
                Exportar por tipo
            </template>
            <b-form-group label="Escolha o formato:">
                <b-form-radio v-model="exportFormat" value="yolo"> YOLO </b-form-radio>
                <b-form-radio v-model="exportFormat" value="faster"> Faster R-CNN </b-form-radio>
            </b-form-group>
            <b-form-group label="Tipos de labels que serão extraídos:">
                <b-form-checkbox v-for="item in items" :key="item.id" v-model="item.selected">
                    {{ item.description }}
                </b-form-checkbox>
            </b-form-group>
        </b-modal>
    </div>
</template>
<script>
import axios from 'axios'

export default {
    name: 'menuHeader',
    props: ['controlButtons'],
    data() {
        return {
            userPrivileged: false,
            training: {
                dataset: '/mnt/oc_datasets',
                nclasses: 1,
                epochs: 10,
                device: 'cpu',
                batch_size: 1,
            },
            faq: {
                question: '',
                answer: '',
            },
            faqs: [],
            logs: [],
            logFields: [
                { 'key' : 'file', 'label' : 'Arquivos', 'sortable' : true},
            ],
            items: [],
            exportFormat: 'yolo',
        }
    },
    created() {
        if (this.$session.exists()) {
            this.userPrivileged = this.$session.get('user_privileged');
        }
    },
    methods: {
        insertDatabase() {
            axios.put(this.backend + '/folders/insert_database').then(res => {
                if (res.status === 200) {
                    this.$bvToast.toast('Inserido no banco com sucesso.', {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                console.log(err);
                this.$bvToast.toast('Não foi possível inserir as informações no banco.', {
                    title: 'Erro durante inserção',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
        showFaqModal() {
            axios.get(this.backend + '/faq').then(res => {
                console.log(res);
                this.faqs = res.data.data;
                this.$bvModal.show('faq-modal');
            }).catch(err => console.log(err));
        },
        showInsertFaqModal() {
            this.$bvModal.show('insert-faq-modal');
        },
        showLogModal() {
            axios.get(this.backend + '/train/log').then(res => {
                console.log(res);
                this.logs = res.data.data;
                this.$bvModal.show('log-modal');
            }).catch(err => console.log(err));
        },
        showTrainModal() {
            this.$bvModal.show('train-modal');
        },
        train() {
            console.log(this.training);
            axios.post(this.backend + '/train', this.training).then(res => {
                if (res.status === 200) {
                    this.$bvToast.toast('Treinamento iniciado!', {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                console.log(err)
                this.$bvToast.toast(`Não foi possível iniciar o treinamento. ${err}.`, {
                    title: 'Erro ao iniciar treinamento.',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
        insertFaq() {
            axios.post(this.backend + '/faq', this.faq).then(res => {
                if (res.status === 200) {
                    this.$bvToast.toast('FAQ inserido!', {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                console.log(err)
                this.$bvToast.toast(`Não foi possível inserir o FAQ. ${err}.`, {
                    title: 'Erro ao inserir FAQ.',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
        exportAll() {
            this.$root.$emit('export-all');
        },
        showExportByTypeModal() {
            this.items = [];
            axios.get(this.backend + '/items').then(res => {
                if (res.data)
                    res.data.items.forEach(el => {
                        el.selected = false;
                        this.items.push(el);
                    });
                this.$bvModal.show('export-by-type-modal');
            }).catch((err) => console.log(err));
        },
        exportByType() {
            let items = [];
            this.items.forEach(el => {if (el.selected)  items.push(el.id)});
            axios.put(this.backend + '/folders/export_by_type', {
                format: this.exportFormat,
                'items': items,
            }).then(res => {
                if (res.status === 200) {
                    this.$bvToast.toast('Imagens exportadas com sucesso!', {
                        title: 'Sucesso!',
                        variant: 'success',
                        autoHideDelay: 5000,
                        appendToast: true,
                    });
                }
            }).catch(err => {
                console.log(err)
                this.$bvToast.toast(`Não foi possível exportar as imagens. ${err}.`, {
                    title: 'Erro ao exportar.',
                    variant: 'danger',
                    noAutoHide: true,
                    appendToast: true,
                });
            });
        },
        doLogout() {
            this.$session.destroy();
            this.$router.push("/login");
        },
    },
}
</script>

<style scoped>

.header {
    min-height: 7%;
    min-height: 7vh;
    max-height: 7%;
    max-height: 7vh;
    height: 7%;
}

.simple-border {
    border: 1px solid #000;
}

.justify-text {
    text-align: justify;
    text-justify: inter-word;
    word-wrap: break-word;
}

</style>