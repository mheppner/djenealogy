'use strict';

(function(angular) {
    
    angular.module('djenealogy.directives.tree', [])
    
        .directive('pedigreeTree', [
            '$window',
            'APP_URL',
            '$timeout',
            'IndividualSrvc',
            '$rootScope',
            function($window,
                    APP_URL,
                    $timeout,
                    IndividualSrvc,
                    $rootScope) {
                return {
                    templateUrl: APP_URL + 'templates/tree/pedigree.html',
                    scope: {
                        treedata: '=',
                    },
                    link: function(scope, elem, attrs) {
                        var tree_el = null,
                            // width of a node
                            leaf = 0,
                            // dimensions for objects
                            tree = { width: 0, height: 0 },
                            container = { width: 0, height: 0 },
                            padding = { horizontal: 0, vertical: 0 },
                            
                            /**
                             * Sets tree element by searching within directive's element.
                             */
                            setTreeEl = function() {
                                tree_el = elem.find('.tree-inner').first();
                            },
                            
                            /**
                             * Sets padding around tree to fill in space within container.
                             * This gives additional area to click and drag on around the
                             * actual tree.
                             */
                            setPadding = function() {
                                // padding should be at least half size of container
                                padding.horizontal = container.width / 2;
                                padding.vertical = container.height / 2;
                                
                                // if container is larger than tree, add additional space
                                if (container.width > tree.width + leaf) {
                                    padding.horizontal += (container.width - (tree.width + leaf)) / 2;
                                }
                                if (container.height > tree.height) {
                                    padding.vertical += (container.height - tree.height) / 2;
                                }
                                
                                tree_el.css({
                                    'padding-top': padding.vertical,
                                    'padding-right': padding.horizontal + leaf,
                                    'padding-bottom': padding.vertical,
                                    'padding-left': padding.horizontal,
                                });
                            },
                            
                            /**
                             * Saves the width and height values for the container,
                             * the tree, and a node.
                             */
                            setWH = function() {
                                // set the container element's height to match the viewport height
                                tree_el
                                    .parent()
                                    .parent()
                                    .height(angular.element($window).innerHeight() - 40);
                                
                                container.width = tree_el.parent().width();
                                container.height = tree_el.parent().height();
                                tree.width = tree_el.width();
                                tree.height = tree_el.height();
                                leaf = tree_el.find('.tree-label').first().outerWidth();
                            },
                            
                            /**
                             * Centers the tree vertically and moves it to the left side
                             * of the root node.
                             */
                            center = function() {
                                tree_el.css('top', - ((tree.height - container.height) / 2 + padding.vertical));
                                tree_el.css('left', - padding.horizontal);
                            }
                        ;
                        
                        
                        // params for jquery ui draggable
                        scope.draggableOptions = {
                            cursor: 'move',
                        };
                        scope.draggableParams = {
                            onStart: 'onStartDrag',
                            onStop: 'onStopDrag',
                            onDrag: 'onDrag',
                        };
                        
                        scope.onStartDrag = function(e, ui) {
                           
                        };
                        
                        scope.onDrag = function(e, ui) {
                            // prevent dragging if going beyond padding area around tree
                            if (// top edge
                                (ui.position.top >= 0) ||
                                // right edge
                                (ui.position.left <= - (padding.horizontal * 2 + leaf + tree.width - container.width)) ||
                                // bottom edge
                                (ui.position.top <= - ( padding.vertical * 2 + tree.height - container.height)) ||
                                // left edge
                                (ui.position.left >= 0)) {
                               
                                e.preventDefault();
                            }
                        };
                        
                        scope.onStopDrag = function(e, ui) {
                           
                        };
                        
                        
                        scope.clickIndv = function(indv) {
                            $rootScope.$broadcast('pedigreeTreeIndividualClick', indv);
                        };
                        
                        angular.element($window).bind('resize', function (){
                            setWH();
                            setPadding();
                            scope.$apply();
                        });
                        
                        $rootScope.$on('pedigreeTreeAdjust', function() {
                            setTreeEl();
                            setWH();
                            setPadding();
                        });
                        
                        $rootScope.$on('pedigreeTreeCenter', function() {
                            center();
                        });
        
                        
                        
                        $timeout(function(){
                            // wait for dom load and set initial tree
                            setTreeEl();
                            setWH();
                            setPadding();
                            center();
                        }, 0);
                    }
                };
            }
        ])

        ;
    
})(angular);
