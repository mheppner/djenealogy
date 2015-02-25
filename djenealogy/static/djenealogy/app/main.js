'use strict';

(function(angular, jQuery) {
    var authInfo;
    angular.element(document).ready(function() {
        angular.bootstrap(document, ['djenealogy']);
        
    });
    
    angular.module('djenealogy.controllers',[]);
    angular.module('djenealogy.services', []);
    
    angular.module('djenealogy', [
            'ngAnimate',
            'ngResource',
            'ngTouch',
            'ngCookies',
            
            'ui.router',
            'ui.utils',
            'ui.bootstrap',
            'oc.lazyLoad',
            'ngStorage',
            
            'djenealogy.services',
            'djenealogy.controllers',
        ])
    
        .run([
            '$rootScope',
            '$state',
            '$stateParams',
            '$location',
            '$log',
            'URLS',
            'STATIC_URL',
            'APP_URL',
            'DEBUG',
            '$ocLazyLoad',
            '$modal',
            '$localStorage',
            function($rootScope,
                     $state,
                     $stateParams,
                     $location,
                     $log,
                     URLS,
                     STATIC_URL,
                     APP_URL,
                     DEBUG,
                     $ocLazyLoad,
                     $modal,
                     $localStorage) {
                
                // global variables
                $rootScope.$storage = $localStorage;
                $rootScope.$state = $state;
                $rootScope.URLS = URLS;
                $rootScope.APP_URL = APP_URL;
                $rootScope.STATIC_URL = STATIC_URL;
                $rootScope.DEBUG = DEBUG;
                
                // events
                $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
                    if (DEBUG) {
                        $log.info('State transition', toState, toParams, fromState, fromParams);
                    }
                });
                
                $rootScope.$on('$stateNotFound', function(event, unfoundState, fromState, fromParams) {
                    if (DEBUG) {
                        $log.error('State not found', unfoundState);
                    }
                    //$state.go('404');
                    //event.preventDefault();
                });
                
                $rootScope.$on('$stateChangeError', function(event, toParams, fromState, fromParams, error) {
                    if (DEBUG) {
                        $log.error('State transition error', event);
                    }
                    
                    $modal.open({
                        templateUrl: 'errorMessage.html',
                        size: 'sm',
                        backdrop: 'static',
                        keyboard: false,
                    });
                });
                
                $rootScope.$on('ocLazyLoad.moduleLoaded', function(e, module) {
                    // load additional modules here
                });
            }
        ])
        
        .config([
            '$stateProvider', 
            '$urlRouterProvider',
            '$httpProvider',
            '$resourceProvider',
            '$ocLazyLoadProvider',
            'STATIC_URL',
            'APP_URL',
            'MODULES',
            'DEBUG',
            function($stateProvider,
                     $urlRouterProvider,
                     $httpProvider,
                     $resourceProvider,
                     $ocLazyLoadProvider,
                     STATIC_URL,
                     APP_URL,
                     MODULES,
                     DEBUG) {
                
                // django configuration
                $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
                $resourceProvider.defaults.stripTrailingSlashes = false;
                
                // default to root state
                $urlRouterProvider.otherwise('/');
                
                // alias the template service provider to set the default paths
                var T = function(file) {
                        return file; //PathServiceProvider.generate(TEMPLATE_PATH, file, CACHE_VERSION);
                    };
                
                // add modules to lazy load
                $ocLazyLoadProvider.config({
                    debug: DEBUG,
                    events: true,
                    modules: MODULES,
                });
                
                
                $stateProvider
                    .state('404', {
                        title: 'Not found',
                        url: '/404',
                        templateUrl: APP_URL + 'templates/404.html',
                    })
                    
                    .state('landing', {
                        title: 'Home',
                        url: '/',
                        template: '<div></div>',
                    })
                    
                    .state('individuals', {
                        title: 'Individuals',
                        url: '/individuals',
                        templateUrl: APP_URL + 'templates/people/list.html',
                        controller: 'PeopleCtrl',
                        resolve: {
                            loadCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    'djenealogy.controllers.people',
                                    'ngTable',
                                ]);
                            }]
                        }
                    })
                    
                    .state('individual', {
                        title: 'Individual',
                        url: '/individuals/:id',
                        templateUrl: APP_URL + 'templates/people/individual.html',
                        controller: 'IndividualCtrl',
                        resolve: {
                            individual: ['IndividualSrvc', '$stateParams', function(IndividualSrvc, $stateParams) {
                                return IndividualSrvc.get({id: $stateParams.id}).$promise;
                            }],
                            loadCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    'djenealogy.controllers.people',
                                ]);
                            }]
                        }
                    })
                    
                    .state('families', {
                        title: 'Families',
                        url: '/families',
                        templateUrl: APP_URL + 'templates/families/list.html',
                        controller: 'FamiliesCtrl',
                        resolve: {
                            loadCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    'djenealogy.controllers.families',
                                    'ngTable',
                                ]);
                            }]
                        }
                    })
                    
                    .state('family', {
                        title: 'Family',
                        url: '/families/:id',
                        templateUrl: APP_URL + 'templates/families/family.html',
                        controller: 'FamilyCtrl',
                        resolve: {
                            family: ['FamilySrvc', '$stateParams', function(FamilySrvc, $stateParams) {
                                return FamilySrvc.get({id: $stateParams.id}).$promise;
                            }],
                            loadCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    'djenealogy.controllers.families',
                                ]);
                            }]
                        }
                    })
                    
                ;
            }
        ]);
        
})(angular, jQuery);