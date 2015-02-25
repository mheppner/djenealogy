'use strict';

(function(angular) {
    angular.module('djenealogy.controllers')

        .controller('NavbarCtrl', [
                '$scope',
                '$state',
            function($scope,
                    $state) {
                 
                $scope.template = $scope.APP_URL + 'templates/common/navbar.html';
                
            }
        ])
        
        .controller('FooterCtrl', ['$scope', 
            function($scope) {
                $scope.template = $scope.APP_URL + 'templates/common/footer.html';
                $scope.year = new Date().getFullYear();
            }
        ])
        
        .controller('LandingCtrl', ['$scope', '$state', 'courses',
            function($scope, $state, courses) {
                $scope.courses = courses;
            }
        ])
    ;

})(angular);