class Canvas {
  constructor (id) {
    this.canvas = document.getElementById(id);
    this.canvas.width = this.canvas.clientWidth * .8;
    this.canvas.height = this.canvas.clientHeight * .8;
    this.elements = []
    this.canvas.addEventListener('touchstart', e => {   
      let {x, y} = this.getMousePos(e);
      this.elements.some(p => p.click(x, y));
    }, false);
  }

  addElement (element) {
    this.elements.push(element);
    this.elements.sort((a, b) => {
      return a.z - b.z;
    })
    this.render ();
  }
  getMousePos (e) {
    let rect = this.canvas.getBoundingClientRect(); 
    let x = e.touches[0].pageX - rect.left - scrollX;
    let y = e.touches[0].pageY - rect.top - scrollY;

    x /=  rect.width; 
    y /=  rect.height; 

    x *= this.canvas.width;
    y *= this.canvas.height;
    return {x, y};
  }

  render () {
    const context = this.canvas.getContext('2d');
    context.fillStyle = 'white';
    context.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.elements.forEach(e => {
      e.draw();
    });
  }
}

class Square {
  constructor (center, width, height, Canvas) {
    this.center = center;
    this.width = width;
    this.height = height;
    this.Canvas = Canvas;
    this.Canvas.addElement(this);
  }

  click () {}

  draw () {
    let context = this.Canvas.canvas.getContext('2d');
    context.beginPath();
    let halfWidth = this.width / 2;
    let halfHeight = this.height / 2;
    context.rect(
      this.center.x - halfWidth, this.center.y - halfHeight, 
      this.width, this.height
    );
    context.stroke();
  }
}

class Curve {
  constructor (start, end, ctrl1, ctrl2, Canvas, elements) {
    this.z = 0;
    this.Canvas = Canvas;
    this.start = start;
    this.end = end;
    this.ctrl1 = ctrl1;
    this.ctrl2 = ctrl2;
    this.Canvas.addElement(this);
  }

  click (x, y) {}

  draw () {
    let context = this.Canvas.canvas.getContext('2d')
    context.beginPath();
    context.moveTo(this.start.x, this.start.y);
    context.bezierCurveTo(
      this.ctrl1.x, this.ctrl2.y,
      this.ctrl1.x, this.ctrl2.y,
      this.end.x, this.end.y
    );
    context.stroke();
  }
}

class Line {
  constructor (start, end, Canvas) {
    this.z = 0;
    this.start = start;
    this.end = end;
    this.posFunc = (start, end) => ({start, end});
    this.style = [];
    this.color = "black";
    this.Canvas = Canvas;
    this.Canvas.addElement(this);
  }

  click (x, y) {}

  pos (callback) {
    this.posFunc = callback;
  }

  draw () {
    let context = this.Canvas.canvas.getContext('2d');
    let {start, end} = this.posFunc (this.start, this.end);
    context.beginPath();
    context.setLineDash(this.style);
    context.moveTo(start.x, start.y);
    context.lineTo(end.x, end.y);
    context.strokeStyle = this.color;
    context.stroke();
    context.setLineDash([]);
  }
}

class Text {
  constructor (Canvas) {
    this.posFunc =  _ => ({x: 0, y: 0});
    this.textFunc = _ => "Text";
    this.color = "black";
    this.size = 20;
    this.Canvas = Canvas;
    this.Canvas.addElement(this);
  }

  click (x, y) {}

  draw () {
    let {x, y} = this.posFunc();
    let context = this.Canvas.canvas.getContext("2d");
    context.font = this.size + "px Arial";
    context.fillStyle = this.color;
    context.fillText(this.textFunc(), x, y);
  }

  pos (callback) {
    this.posFunc = callback;
  }

  text (callback) {
    this.textFunc = callback;
  }

}


class Point {
  constructor (x, y, Canvas) {
    this.z = 10;
    this.Canvas = Canvas;
    this.onDragCallback = _ => {};
    this.x = x;
    this.y = y;
    this.radius = 7
    this.Canvas.addElement(this);
  }

  click (x, y) {
    const distance = Math.hypot(x - this.x, y - this.y);
    if (distance <= this.radius) {
      this.startDragging();
      return true;
    }
      return false;
  }

  draw () {
    let context = this.Canvas.canvas.getContext('2d');
    context.beginPath();
    context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
    context.fillStyle = 'black';
    context.fill();
    context.stroke();
  }

  startDragging () {
    let canvas = this.Canvas.canvas;
    this.draggingBound = this.dragging.bind(this);
    canvas.addEventListener('touchmove', this.draggingBound);
    canvas.addEventListener('touchend', e => {
      canvas.removeEventListener('touchmove', this.draggingBound);
    });
  } 

  dragging (e) {
    e.preventDefault();
    let {x, y} = this.Canvas.getMousePos(e);
    this.x = x;
    this.y = y;
    this.onDragCallback(x, y);
    this.Canvas.render();
  }

  onDrag (callback) {
    this.onDragCallback = callback;
  }


}