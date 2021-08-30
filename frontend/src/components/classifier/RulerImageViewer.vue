<template>
    <canvas ref="canvas"> </canvas>
</template>

<script>
import { fabric } from 'fabric';

const IMAGE_WIDTH = 1920;
const IMAGE_HEIGHT = 1080;

export default {
    name: 'rulerImageViewer',
    data() {
        return {
            canvas: null,
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
        updateImage(currentImage) {
            // this.deleteAllObjects();
            console.log("updateImage-RulerImageViwer");
            fabric.Image.fromURL('data:image/jpeg;base64,' + currentImage.data, (image) => {
                this.canvas.setBackgroundImage(image, this.canvas.renderAll.bind(this.canvas));
                this.windowResize();
                // if (currentImage.labels) this.drawLabels(currentImage, items);
                this.$emit('updateLoaded', true);
                this.canvas.renderAll();
            });
        },
        // addObject() {
        //     var height, width, top, left;
        //     height = width = top = left = 100;

        //     const rect = new fabric.Rect({
        //         height: height,
        //         width: width,
        //         fill: `#${item.color}`,
        //         lockRotation: true,
        //         hasRotationPoint: false,
        //         opacity: 0.6,
        //     });
        //     rect.setControlsVisibility({mtr:false});
        //     const text = new fabric.Text(item.description, {
        //         fontSize: 20,
        //         fill: '#ffffff',
        //         originX: 'left',
        //         originY: 'top',
        //     });
        //     const group = new fabric.Group([rect, text], {
        //         top: top,
        //         left: left,
        //     });
        //     this.canvas.add(group);
        addObject() {
            var left, top;
            left = top = 100;
            const line = new fabric.Line([60, 100, 300, 100], {
                // left: 470,
                // top: 550,
                strokeWidth: 5,
                stroke: 'red',
                lockRotation: true,
                hasRotationPoint: false,
            });
            line.setControlsVisibility({mtr:false})
            const text = new fabric.Text( 'Régua', {
                fontSize: 20,
                fill: '#ffffff',
                originX: 'left',
                originY: 'top',
            });
            const group = new fabric.Group([line, text], {
                top: top,
                left: left,
            });
            this.canvas.add(group);
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
                    lockRotation: true,
                    hasRotationPoint: false,
                    opacity: 0.6,
                });
                rect.setControlsVisibility({mtr:false});
                const text = new fabric.Text(item.description, {
                    fontSize: 20,
                    fill: '#ffffff',
                    originX: 'left',
                    originY: 'top',
                });
                const group = new fabric.Group([rect, text], {
                    top: Math.round((el.y_center - (el.height / 2)) * heightRatio),
                    left: Math.round((el.x_center - (el.width / 2)) * widthRatio),
                });
                this.canvas.add(group);
            });
        },
    }
}
        // clickEvent(event) {
        //     if (firstClick) {
        //         var rect = event.target.getBoundingClientRect();
        //         var x = event.clientX - rect.left;
        //         var y = event.clientY - rect.top;
        //         firstClick = true;
        //         console.log(x)
        //         console.log(y)
        //     }
        // },
</script>

<style scoped>

</style>
