$('.otree-btn-next').hide();

function Category(id, otree_field_rel_id, otree_field_abs_id, order) {
    this.otree_field_rel_id = otree_field_rel_id;
    this.otree_field_abs_id = otree_field_abs_id;

    this.id = id;
    this.order = order;
    this.dropped = false;
    
    this.left_fixed = (this.order == 1);
    this.right_fixed = (this.order == 5);

    this.width = 180;
    this.label_min_size = 20;

    this.handle_left = this.right_fixed;

    var self = this;

    this.drop = function() {
        this.dropped = true;  
        this.draggable_off();
        //if (!this.right_fixed) {
            this.resizable_on();
        // }
        this.update_otree_field();
    }

    this.connect_to_element = function () {
        this.container_element = $('#'+this.id);
        this.container_element.children('.label').disableSelection();
        this.container_element.disableSelection();
        this.container_element.on('resizestart', function (event, ui) {
            self.cm.resize_start(self, ui.size.width);
        });
        this.container_element.on('resize', function (event, ui) {
            self.update_width();
            var delta = ui.size.width - ui.originalSize.width;
            self.cm.resize(self, delta);
            // console.log(self.cm.fraction_range(self));
            self.update_otree_field();
        });
        this.container_element.on('resizestop', function(event, ui) {
            if (self.order == 5 && self.cm.absolute_range(self)['high'] >= 999.9) {
                self.resizable_off();
                self.cm.activate_next();
            }
        });
    }

    this.update_otree_field = function () {
        $('#'+this.otree_field_rel_id).val(this.cm.fraction_range(this)['high']);
        $('#'+this.otree_field_abs_id).val(Math.round(this.cm.absolute_range(this)['high']));
    }

    this.draggable_on = function () {
        this.container_element.draggable({'cursor': 'move', revert: 'invalid'});
        this.container_element.children('.label').addClass('draggablelabel');
    }

    this.draggable_off = function () {
        this.container_element.draggable({disabled: true});
        this.container_element.children('.label').removeClass('draggablelabel');
    }

    this.resizable_on = function () {
        this.container_element.resizable({minWidth: this.label_min_size, minHeight: 25, maxHeight: 25, handles: "e"});
        this.container_element.children('.category_label_handle').addClass('resize_handle');
    }

    this.resizable_off = function () {
        this.container_element.resizable({disabled: true});
        this.container_element.children('.category_label_handle').removeClass('resize_handle');
    }

    this.set_pos = function (target_pos) {
        this.container_element.position({my: "left top", at: target_pos, of: "#axis"});
    }

    this.update_width = function () {
        this.width = this.container_element.width();
    }

    this.set_width = function (width) {
        this.width = width;
        this.container_element.width(this.width);
    }

    this.handle_left = function () {
        this.container_element.children(".category_label_handle").removeClass('handle_right');
        this.container_element.children(".category_label_handle").hide()
    }

    this.set_cm = function(category_manager) {
        this.cm = category_manager;
    }

    this.set_max_width = function (max_width) {
        this.container_element.resizable({maxWidth: max_width});
    }

    this.left_value = function () {
        return this.container_element.position().left;
    }

    this.right_value = function () {
        return this.width + this.container_element.position().left;
    }

    // construct!
    this.connect_to_element();

}

function CategoryManager(list_of_elements, axis_id) {
    this.catlist = list_of_elements;
    this.dropped = [];

    self = this;

    this.element_by_id = function (id) {
        for (var e in this.catlist) {
            if (this.catlist[e].id == id) {
                return this.catlist[e];
            }
        }
    }

    this.activate_next = function () {
        $('.otree-btn-next').show();
    }

    this.successor_by_element = function (element) {
        for (var e in this.catlist) {
            if (this.catlist[e] == element) {
                return this.catlist[parseInt(e)+1];
            }
        }
    }

    this.dropped_successor_by_element = function (element) {
        for (var e in this.dropped) {
            if (this.dropped[e] == element) {
                return this.dropped[parseInt(e)+1];
            }
        }
    }

    this.predecessor_by_element = function (element) {
        for (var e in this.catlist) {
            if (this.catlist[e] == element) {
                return this.catlist[parseInt(e)-1];
            }
        }
    }

    this.successor_by_id = function (id) {
        for (var e in this.catlist) {
            if (this.catlist[e].id == id) {
                return this.catlist[e+1];
            }
        }
    }

    this.drop = function (id) {
        var target = this.element_by_id(id);
        var successor = this.successor_by_element(target);
        
        // keep track of dropped
        this.dropped.push(target);

        // handle target, first drop, then resize
        target.drop();

        // figure out how much space is occupied
        var occupied_space = this.left_sum();

        if (target.left_fixed) {
            target.set_pos("left top");
        }

        if (!target.left_fixed) {
            // then position left top at the edge
            var new_pos = "left+"+occupied_space+" top";
            target.set_pos(new_pos);


            var remaining_space = this.axis.width() - occupied_space - target.width;

            if (remaining_space < 0) {
                var new_width = target.width + remaining_space - (6-this.dropped.length)*target.label_min_size;
                target.set_width(new_width);
            }

        }

        target.update_otree_field();

        // if (target.right_fixed) {
        //     // it has already snapped left, now resize
        //     var remaining_space = this.axis.width() - occupied_space;
        //     target.set_width(remaining_space);
        //     target.handle_left();
        // }

        // handle successor if exisiting
        if (successor !== undefined) {
            successor.draggable_on();
        }

    }

    this.resize = function (category_element, delta_w) {
        var target = category_element;
        var predecessor = this.predecessor_by_element(target);
        var successor = this.dropped_successor_by_element(target);

        // if we have a successor
        if (successor !== undefined) {
            if (successor.start_width - delta_w > successor.label_min_size) {
                successor.set_width(successor.start_width - delta_w);

                var occupied_space = this.left_sum(successor.order);
                var new_pos = "left+"+occupied_space + " top";
                successor.set_pos(new_pos);

                //successor.update_otree_field();
            }                       
        }
    }

    this.resize_start = function (category_element, start_width) {
        var target = category_element;
        var predecessor = this.predecessor_by_element(target);
        var successor = this.dropped_successor_by_element(target);

        target.start_width = target.width;

        if (successor !== undefined) {
            successor.start_width = successor.width;
            var target_max_width = target.start_width + successor.start_width - successor.label_min_size;
            target.set_max_width(target_max_width);
        } else {
            var occupied_space = this.left_sum();
            var remaining_space = this.axis.width() - occupied_space - target.start_width;
            // console.log(remaining_space);

            var drop_multi = 6;
            if (target.order == 5) {
                drop_multi -= 1;
            }

            var target_max_width = target.start_width - (drop_multi - this.dropped.length)*target.label_min_size + remaining_space;
            target.set_max_width(target_max_width);
        }

        if (predecessor !== undefined) {
            predecessor.start_width = predecessor.width;
        }
    }

    this.absolute_range = function (target) {
        var first_element = this.dropped[0];
        var left_offset = first_element.container_element.position().left;
        var low_value = target.container_element.position().left - left_offset;
        var high_value = low_value + target.width;
        var dif = high_value - low_value;
        return { low: low_value, high: high_value, dif: dif };
    }

    this.fraction_range = function (target) {
        var abs_range = this.absolute_range(target);
        var low_rel = abs_range.low / this.axis.width();
        var high_rel = abs_range.high / this.axis.width();
        var dif = high_rel - low_rel;
        return { low: low_rel, high: high_rel, dif: dif };
    }

    this.left_sum = function (up_to) {
        var sum = 0;
        if (up_to === undefined) {
            for (var e = 0; e < this.dropped.length-1; e++) {
                sum += this.dropped[e].width;
            }
        } else {
            for (var e = 1; e < up_to; e++) {
                sum += this.dropped[e-1].width;
            }
        }
        return sum;
    }

    this.setup_axis = function (axis_id) {
        this.axis = $(axis_id);
        this.axis.droppable({accept: '.category_label' });

        this.axis.on('drop', function(event, ui) {
            self.drop(ui.draggable[0].id);
        });
    }

    // prep axis
    this.setup_axis(axis_id);

    // set category manager on category elements
    for (var e in this.catlist) {
        this.catlist[e].set_cm(this);
    }

    // activate first element
    this.catlist[0].draggable_on();

}


// Generate Category Elements
var a = new Category("a", "id_cat_end_rel_1", "id_cat_end_abs_1", 1);
var b = new Category("b", "id_cat_end_rel_2", "id_cat_end_abs_2", 2);
var c = new Category("c", "id_cat_end_rel_3", "id_cat_end_abs_3", 3);
var d = new Category("d", "id_cat_end_rel_4", "id_cat_end_abs_4", 4);
var e = new Category("e", "id_cat_end_rel_5", "id_cat_end_abs_5", 5);

var CM = new CategoryManager([a, b, c, d, e], '#axis');
