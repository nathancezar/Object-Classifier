<template>
    <canvas ref="canvas"> </canvas>
</template>

<script>
import { fabric } from 'fabric';

const IMAGE_WIDTH = 1920;
const IMAGE_HEIGHT = 1080;
const DRAINAGE = 4;
const CLEARING = 5;
const GUARDRAIL = 7;
const NEWJERSEY = 8;

export default {
    name: 'imageViewer',
    data() {
        return {
            canvas: null,
            previousDrainage: null,
            previousGuadRail: null,
            previousNewJersey: null,
        }
    },
    mounted() {
        this.$nextTick(() => {
            window.addEventListener('resize', this.windowResize);

            this.canvas = new fabric.Canvas(this.$refs.canvas, {
                lockUniScaling: false,
                uniScaleTransform: true,
            });

            this.canvas.on('object:modified', (event) => {
                const object = event.target;
                if (!object) return;
                object.setCoords();
                if (object.top < 0) object.top = 0;
                if (object.left < 0) object.left = 0;
                if (object.left + (object.width * object.scaleX) > this.canvas.width)
                    object.scaleX = (this.canvas.width - object.left) / object.width;
                if (object.top + (object.height * object.scaleY) > this.canvas.height)
                    object.scaleY = (this.canvas.height - object.top) / object.height;
                object.setCoords();

                const group = event.transform.target;
                const text = event.transform.target.item(1);
                if (group && text) {
                    text.set('scaleX', group.width / (group.width * group.scaleX));
                    text.set('scaleY', group.height / (group.height * group.scaleY));
                }
            });

            this.canvas.on('object:moving', (event) => {
                const object = event.target;
                if (!object) return;
                object.setCoords();
                if (object.top < 0) object.top = 0;
                if (object.left < 0) object.left = 0;
                if (object.left + (object.width * object.scaleX) > this.canvas.width)
                    object.left = this.canvas.width - (object.width * object.scaleX);
                if (object.top + (object.height * object.scaleY) > this.canvas.height)
                    object.top = this.canvas.height - (object.height * object.scaleY);
                object.setCoords();
            });

            this.canvas.on('selection:created', (event) => {
                event.target.set({hasRotatingPoint: false});
            })

            this.canvas.on('selection:updated', (event) => {
                event.target.set({hasRotatingPoint: false});
            })
        });
    },
    methods: {
        windowResize() {
            if (this.canvas) {
                const width = document.documentElement.clientWidth * 5 / 6;
                const height = IMAGE_HEIGHT / IMAGE_WIDTH * width;
                this.canvas.setWidth(width);
                this.canvas.setHeight(height);
                if (this.canvas.backgroundImage) {
                    this.canvas.backgroundImage.scaleToWidth(width);
                    this.canvas.backgroundImage.scaleToHeight(height);
                }
            }
        },
        updateImage(currentImage, items) {
            this.deleteAllObjects();
            fabric.Image.fromURL('data:image/jpeg;base64,' + currentImage.data, (image) => {
                this.canvas.setBackgroundImage(image, this.canvas.renderAll.bind(this.canvas));
                this.windowResize();
                if (currentImage.labels) this.drawLabels(currentImage, items);
                this.$emit('updateLoaded', true);
                this.canvas.renderAll();
            });
        },
        addObject(item) {
            var height, width, top, left;
            height = width = top = left = 100;
            if (item.id === CLEARING) {
                height = 250;
                width = 250;
            } else if (item.id === DRAINAGE && this.previousDrainage) {
                height = this.previousDrainage.height * this.previousDrainage.scaleY;
                width = this.previousDrainage.width * this.previousDrainage.scaleX;
                top = this.previousDrainage.top;
                left = this.previousDrainage.left;
            } else if (item.id === GUARDRAIL && this.previousGuadRail) {
                height = this.previousGuadRail.height * this.previousGuadRail.scaleY;
                width = this.previousGuadRail.width * this.previousGuadRail.scaleX;
                top = this.previousGuadRail.top;
                left = this.previousGuadRail.left;
            } else if (item.id === NEWJERSEY && this.previousNewJersey) {
                height = this.previousNewJersey.height * this.previousNewJersey.scaleY;
                width = this.previousNewJersey.width * this.previousNewJersey.scaleX;
                top = this.previousNewJersey.top;
                left = this.previousNewJersey.left;
            }
            const rect = new fabric.Rect({
                height: height,
                width: width,
                fill: `#${item.color}`,
                hasRotationPoint: false,
                opacity: 0.6,
            });
            rect.setControlsVisibility({mtr:false});
            const text = new fabric.Text(item.description, {
                fontSize: 20,
                fill: '#ffffff',
                originX: 'left',
                originY: 'top',
                hasRotationPoint: false,
            });
            const group = new fabric.Group([rect, text], {
                top: top,
                left: left,
                hasRotationPoint: false,
            });
            this.canvas.add(group);
        },
        deleteSelectedObject() {
            const selection = this.canvas.getActiveObject();
            if (!selection) return;
            if (selection.type === 'activeSelection') {
                this.canvas.remove(...selection.getObjects());
            } else {
                this.canvas.remove(selection);
            }
            this.canvas.discardActiveObject();
            this.canvas.renderAll();
        },
        deleteAllObjects() {
            this.canvas.remove(...this.canvas.getObjects());
            this.canvas.discardActiveObject();
            this.canvas.renderAll();
        },
        getLabels(items) {
            const labels = []

            const widthRatio = IMAGE_WIDTH / this.canvas.width;
            const heightRatio = IMAGE_HEIGHT / this.canvas.height;

            this.canvas.getObjects().forEach((object) => {
                let width = object.width * widthRatio * object.scaleX;
                let height = object.height * heightRatio * object.scaleY;

                let left = object.left * widthRatio;
                let top = object.top * heightRatio;
                if (left + width > IMAGE_WIDTH) width = IMAGE_WIDTH - left;
                if (top + height > IMAGE_HEIGHT) height = IMAGE_HEIGHT - top;

                let item_id = items.find(element => element.description === object.getObjects()[1].text).id;
                if (item_id === DRAINAGE) this.previousDrainage = object;
                if (item_id === GUARDRAIL) this.previousGuadRail = object;
                if (item_id === NEWJERSEY) this.previousNewJersey = object;
                labels.push({
                    'item_id': item_id,
                    'width': Math.round(width),
                    'height': Math.round(height),
                    'x_center': Math.round(left + (width / 2)),
                    'y_center': Math.round(top + (height / 2)),
                });
            });
            return labels;
        },
        drawLabels(currentImage, items) {
            const widthRatio =  this.canvas.width / IMAGE_WIDTH;
            const heightRatio = this.canvas.height / IMAGE_HEIGHT;

            currentImage.labels.forEach(el => {
                const item = items.find(item => item.id === el.item_id);
                const rect = new fabric.Rect({
                    height: Math.round(el.height * heightRatio),
                    width: Math.round(el.width * widthRatio),
                    fill: `#${item.color}`,
                    hasRotationPoint: false,
                    opacity: 0.6,
                });
                rect.setControlsVisibility({mtr:false});
                const text = new fabric.Text(item.description, {
                    fontSize: 20,
                    fill: '#ffffff',
                    originX: 'left',
                    originY: 'top',
                    hasRotationPoint: false,
                });
                const group = new fabric.Group([rect, text], {
                    top: Math.round((el.y_center - (el.height / 2)) * heightRatio),
                    left: Math.round((el.x_center - (el.width / 2)) * widthRatio),
                    hasRotationPoint: false,
                });
                this.canvas.add(group);
            });
        },
    }
}
</script>

<style scoped>

</style>
