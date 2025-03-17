/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.heuristic;

import cujae.inf.citi.om.data.BusStop;
import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.solution.Route;
import cujae.inf.citi.om.solution.RouteTTRP;
import cujae.inf.citi.om.solution.RouteType;
import cujae.inf.citi.om.solution.Solution;
import cujae.inf.ic.om.matrix.NumericMatrix;
import java.util.ArrayList;

/**
 *
 * @author nanda
 */
public class KilbyAlgorithm extends Heuristic {

    private ArrayList<Route> listCandidateRoutes;
    private ArrayList<Metric> listKilbyCosts;
    private int countTrailers;
    private CustomerType typeCustomer;
    private ArrayList<Object> listAccessVc;
    private int countVehicles;
    private Operator_3opt threeOpt;
    private Metric metricKilby;
    private int posRoute;
    private boolean isRouteFull;
    private int routesWithElements;
    private ArrayList<Route> listRouteOpt;
    private ProblemType typeProblem;
    private int posDepot;
    private int idDepot;
    private double capacityVehicle;
    private double capacityTrailer;
    private ArrayList<Customer> customersToVisit;
    private ArrayList<BusStop> listBusStops;
    private Solution solution;
    private double capacityTotal;
    private boolean isOpen;

    public KilbyAlgorithm() {
        super();
        this.listCandidateRoutes = new ArrayList<>();
        this.listKilbyCosts = new ArrayList<>();
        this.listAccessVc = new ArrayList<>();
        this.listRouteOpt = new ArrayList<>();
        this.threeOpt = new Operator_3opt();
    }

    @Override
    public void initializeSpecifics() {

        this.listCandidateRoutes = new ArrayList<>();
        this.listKilbyCosts = null;

        this.countTrailers = 0;
        this.typeCustomer = CustomerType.TC;
        this.listAccessVc = new ArrayList<>();

        if (Problem.getProblem().getTypeProblem() == ProblemType.TTRP) {
            this.countTrailers = ((FleetTTRP)Problem.getProblem()
                    .getListDepots().get(this.posDepot)
                    .getListFleets().get(0))
                    .getCountTrailers();
        } else if (Problem.getProblem().getTypeProblem() == ProblemType.HFVRP) {
            this.countVehicles = Problem.getProblem().fillListCapacities(this.posDepot).size();
        } else {
            this.countVehicles = Problem.getProblem()
                    .getListDepots().get(this.posDepot)
                    .getListFleets().get(0)
                    .getCountVehicles();
        }

        this.threeOpt = new Operator_3opt();

        this.metricKilby = null;
        this.posRoute = -1;
        this.isRouteFull = true;
        this.routesWithElements = 0;

        for (int i = 0; i < this.countVehicles; i++) {
            Route route;
            if (this.typeProblem == ProblemType.TTRP) {
                route = new RouteTTRP();
            } else {
                route = new Route();
            }
            this.listCandidateRoutes.add(route);
        }

        this.listRouteOpt = new ArrayList<>();
    }

    public void creating() {
        if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP ||
            this.typeProblem == ProblemType.HFVRP || this.typeProblem == ProblemType.MDVRP ||
            this.typeProblem == ProblemType.TTRP || this.typeProblem == ProblemType.SBRP ||
            this.typeProblem == ProblemType.VRPTW) {

            while (this.listKilbyCosts != null && !this.listKilbyCosts.isEmpty()) {
                int i = 0;
                while (i < this.listCandidateRoutes.size() && !this.listKilbyCosts.isEmpty()) {
                    Customer customer = super.getCustomerByID(
                                this.listKilbyCosts.get(0).getIdElement(),
                                this.customersToVisit
                        );
                        double requestRouteValue = customer.getRequestCustomer();

                        this.listCandidateRoutes.get(i).getListIdCustomers().add(customer.getIdCustomer());
                    

                    this.listCandidateRoutes.get(i).setRequestRoute(requestRoute);
                    this.listCandidateRoutes.get(i).setIdDepot(this.idDepot);
                    this.listKilbyCosts.remove(0);

                    this.customersToVisit.remove(customer);
                    
                    this.routesWithElements++;

                    if (this.typeProblem == ProblemType.TTRP) {
                        if (((CustomerTTRP)customer).getTypeCustomer() == CustomerType.TC) {
                            this.capacityTotal = this.capacityVehicle;
                        } else {
                            this.capacityTotal = this.capacityVehicle + this.capacityTrailer;
                        }
                    }

                    i++;

                    if (this.typeProblem == ProblemType.HFVRP) {
                        this.isOpen = true;
                    }
                }

                int j = this.routesWithElements;

                while (this.routesWithElements < this.listCandidateRoutes.size()) {
                    this.listCandidateRoutes.remove(j);
                }
            }
        }
    }

    public void processing() {
        while (!this.listCandidateRoutes.isEmpty() && !this.customersToVisit.isEmpty()) {
                this.metricKilby = new Metric();
                this.metricKilby = getBestElement(
                        this.idDepot,
                        this.customersToVisit,
                        this.listCandidateRoutes,
                        this.capacityVehicle,
                        this.countTrailers
                );

                if (this.metricKilby == null) {
                    this.posRoute = this.closeRoute(this.listCandidateRoutes);
                    this.isRouteFull = false;
                } else {
                    Customer customerInsert = super.getCustomerByID(
                            this.metricKilby.getIdElement(),
                            this.customersToVisit
                    );

                    this.posRoute = this.metricKilby.getIndex();
                    this.requestRoute = this.listCandidateRoutes.get(this.metricKilby.getIndex()).getRequestRoute() +
                            customerInsert.getRequestCustomer();

                    this.listCandidateRoutes.get(this.posRoute).getListIdCustomers().add(customerInsert.getIdCustomer());
                    this.listCandidateRoutes.get(this.posRoute).setRequestRoute(this.requestRoute);
                    this.listCandidateRoutes.get(this.posRoute).setIdDepot(this.idDepot);
                    this.customersToVisit.remove(customerInsert);

                    this.isRouteFull = requestPerfect(
                            this.customersToVisit,
                            this.capacityVehicle,
                            this.requestRoute
                    );

                    if (this.typeProblem == ProblemType.TTRP) {
                        if (((CustomerTTRP)customerInsert).getTypeCustomer() == CustomerType.VC && ((CustomerTTRP)customerInsert).getTypeCustomer() == CustomerType.TC) {
                            this.isTC = true;
                        }
                    }
                }

                if (!this.isRouteFull) {
                    this.listRouteOpt.add(this.listCandidateRoutes.get(this.posRoute));
                    this.listCandidateRoutes.remove(this.posRoute);
                }

                if (this.typeProblem == ProblemType.TTRP) {
                    if (this.listCandidateRoutes.isEmpty()) {
                        for (int i = 0; i < this.countVehicles; i++) {
                            Route newRoute = new RouteTTRP();
                            this.listCandidateRoutes.add(newRoute);
                        }
                        this.listKilbyCosts = selectBestCost(
                                this.countVehicles,
                                this.countTrailers,
                                this.idDepot,
                                this.customersToVisit
                        );
                        this.creating();
                    }
                }
            }

            while (!this.listCandidateRoutes.isEmpty()) {
                this.posRoute = 0;
                this.listRouteOpt.add(this.listCandidateRoutes.get(this.posRoute));
                this.listCandidateRoutes.remove(this.posRoute);
            }
    }

    @Override
    public Solution execute() {
        if (this.typeProblem == ProblemType.CVRP ||
            this.typeProblem == ProblemType.OVRP ||
            this.typeProblem == ProblemType.VRPTW ) {

            if (!this.customersToVisit.isEmpty()) {
                    this.listKilbyCosts = new ArrayList<>();
                    this.listKilbyCosts = this.selectBestCost(
                            this.countVehicles,
                            this.countTrailers,
                            this.idDepot,
                            this.customersToVisit
                    );

                    this.creating();

                    this.processing();
                }
            

            this.solution.setListRoutes(this.listRouteOpt);
        } else if (this.typeProblem == ProblemType.HFVRP) {
            ArrayList<Double> listCapacities = new ArrayList<>(Problem.getProblem().getListCapacities());
            this.capacityVehicle = listCapacities.get(0);
            boolean isOpen = true;

            if (!this.customersToVisit.isEmpty()) {
                this.listKilbyCosts = new ArrayList<>();
                this.listKilbyCosts = this.selectBestCost(
                        this.countVehicles,
                        this.countTrailers,
                        this.idDepot,
                        this.customersToVisit
                );

                this.creating();

                this.processing();

                while (!this.listCandidateRoutes.isEmpty()) {
                    this.posRoute = 0;
                    if (this.listCandidateRoutes.get(this.posRoute).getListIdCustomers().size() >= 6) {
                        this.threeOpt.toOptimize(this.listCandidateRoutes.get(this.posRoute));
                    }
                    this.listRouteOpt.add(this.listCandidateRoutes.get(this.posRoute));
                    this.listCandidateRoutes.remove(this.posRoute);
                }
            }

            this.solution.setListRoutes(this.listRouteOpt);
            listCapacities.remove(0);
            isOpen = false;

            if (isOpen && !this.customersToVisit.isEmpty()) {
                this.route.setRequestRoute(this.requestRoute);
                this.route.setIdDepot(this.idDepot);
                this.solution.getListRoutes().add(this.route);
            }

            if (!this.customersToVisit.isEmpty()) {
                Route newRoute = new Route();
                double newRequest = 0.0;
                newRoute.setIdDepot(this.idDepot);

                while (!this.customersToVisit.isEmpty()) {
                    newRequest += this.customersToVisit.get(0).getRequestCustomer();
                    newRoute.setRequestRoute(newRequest);
                    newRoute.getListIdCustomers().add(this.customersToVisit.get(0).getIdCustomer());
                    this.customersToVisit.remove(0);
                }

                this.solution.getListRoutes().add(newRoute);
            }

            if (isOpen) {
                this.route.setRequestRoute(this.requestRoute);
                this.route.setIdDepot(this.idDepot);
                this.solution.getListRoutes().add(this.route);
            }
        } else if (this.typeProblem == ProblemType.MDVRP) {
            for (int j = this.posDepot; j < Problem.getProblem().getListDepots().size(); j++) {
                if (j != this.posDepot) {
                    this.idDepot = Problem.getProblem().getListDepots().get(j).getIdDepot();
                    this.customersToVisit = new ArrayList<>(
                            Problem.getProblem().getCustomersAssignedByIDDepot(
                                    this.idDepot,
                                    Problem.getProblem().getListCustomers(),
                                    Problem.getProblem().getListDepots()
                            )
                    );

                    this.capacityVehicle = Problem.getProblem()
                            .getListDepots().get(j)
                            .getListFleets().get(0)
                            .getCapacityVehicle();
                    this.countVehicles = Problem.getProblem()
                            .getListDepots().get(j)
                            .getListFleets().get(0)
                            .getCountVehicles();
                }

                if (!this.customersToVisit.isEmpty()) {
                    this.listKilbyCosts = new ArrayList<>();
                    this.listKilbyCosts = this.selectBestCost(
                            this.countVehicles,
                            this.countTrailers,
                            this.idDepot,
                            this.customersToVisit
                    );

                    this.creating();

                    this.processing();
                }

                this.solution.setListRoutes(this.listRouteOpt);

                for (int i = 0; i < this.countVehicles; i++) {
                    Route newRoute = new Route();
                    this.listCandidateRoutes.add(newRoute);
                }
            }
        } else if (this.typeProblem == ProblemType.TTRP) {
            this.listAccessVc = new ArrayList<>();
            if (!this.customersToVisit.isEmpty()) {
                this.isTC = false;
                this.capacityTrailer = ((FleetTTRP)Problem.getProblem()
                        .getListDepots().get(this.posDepot)
                        .getListFleets().get(0))
                        .getCapacityTrailer();
                this.capacityTotal = 0.0;
                this.typeCustomer = CustomerType.TC;

                this.listKilbyCosts = new ArrayList<>();
                this.listKilbyCosts = this.selectBestCost(
                        this.countVehicles,
                        this.countTrailers,
                        this.idDepot,
                        this.customersToVisit
                );

                this.creating();

                this.processing();
            }

            this.solution.setListRoutes(this.listRouteOpt);
        }
        return this.solution;
    }

    public Solution getSolutionInicial() {
        this.execute();
        return this.solution;
    }

    // Método que devuelve una lista de los n mejores para las n rutas
    public ArrayList<Metric> selectBestCost(int countVehicles, int countTrailers, int idDepot, ArrayList<Customer> listElement) {
        ArrayList<Metric> listKilbyCosts = new ArrayList<>();
        Metric metricKilby = null;
        double costKilby = 0.0;

        int countRoutesPvr = countTrailers;
        int countRoutesPtr = countVehicles - countTrailers;
        CustomerType typeCustomer = null;

        for (int i = 0; i < listElement.size(); i++) {
            metricKilby = new Metric();

            if (listElement.get(i) instanceof CustomerTTRP) {
                    typeCustomer = ((CustomerTTRP) listElement.get(i)).getTypeCustomer();
                } else {
                    typeCustomer = CustomerType.TC;
                }

                costKilby = calculateCostOfKilby(idDepot, idDepot, listElement.get(i).getIdCustomer());

                if (listKilbyCosts.size() < countVehicles) {
                    if ((typeCustomer == CustomerType.VC ) && countRoutesPvr != 0
                            || (typeCustomer == CustomerType.TC ) && countRoutesPtr != 0) {
                        metricKilby.setIdElement(listElement.get(i).getIdCustomer());
                        metricKilby.setInsertionCost(costKilby);

                        listKilbyCosts.add(metricKilby);

                        if (typeCustomer == CustomerType.VC ) {
                            countRoutesPvr--;
                        } else {
                            countRoutesPtr--;
                        }
                    }
                } else {
                    int posMaxCost = findMaxCost(listKilbyCosts, listElement, typeCustomer);

                    if (costKilby < listKilbyCosts.get(posMaxCost).getInsertionCost()) {
                        metricKilby.setIdElement(listElement.get(i).getIdCustomer());
                        metricKilby.setInsertionCost(costKilby);

                        listKilbyCosts.remove(posMaxCost);
                        listKilbyCosts.add(metricKilby);
                    }
                }
            
        }

        return listKilbyCosts;
    }

    // Método que calcula el costo de insertar un cliente en la ruta
    public double calculateCostOfKilby(int idDepot, int currentElement, int nextElement) {
        double costActualToNext = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(currentElement), Problem.getProblem().getPosElement(nextElement));
        double costNextToDepot = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(nextElement), Problem.getProblem().getPosElement(idDepot));
        double costActualToDepot = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(currentElement), Problem.getProblem().getPosElement(idDepot));

        return costActualToNext + costNextToDepot - costActualToDepot;
    }

    // Método que devuelve la posición del mayor costo de la lista
    public int findMaxCost(ArrayList<Metric> listKilbyCosts, ArrayList<Customer> listElements, CustomerType typeCustomer) {
        int posMaxCost = -1;
        double maxCost = 0.0;
        double currentCost = 0.0;
        CustomerType currentTypeCustomer = null;

        ProblemType tp = Problem.getProblem().getTypeProblem();

        if (tp == ProblemType.CVRP || tp == ProblemType.HFVRP || tp == ProblemType.MDVRP || tp == ProblemType.OVRP) {
            posMaxCost = 0;
            maxCost = listKilbyCosts.get(posMaxCost).getInsertionCost();

            for (int i = 1; i < listKilbyCosts.size(); i++) {
                currentCost = listKilbyCosts.get(i).getInsertionCost();

                if (maxCost < currentCost) {
                    maxCost = currentCost;
                    posMaxCost = i;
                }
            }
        } else if (tp == ProblemType.TTRP) {
            posMaxCost = findFirstCustomerEqualsAccess(typeCustomer, listKilbyCosts, listElements);
            maxCost = listKilbyCosts.get(posMaxCost).getInsertionCost();

            for (int i = posMaxCost + 1; i < listKilbyCosts.size(); i++) {
                currentCost = listKilbyCosts.get(i).getInsertionCost();
                currentTypeCustomer = ((CustomerTTRP)getCustomerByID(listKilbyCosts.get(i).getIdElement(), listElements)).getTypeCustomer();

                if (maxCost < currentCost && currentTypeCustomer == typeCustomer) {
                    maxCost = currentCost;
                    posMaxCost = i;
                }
            }
        }

        return posMaxCost;
    }

    // Método que devuelve la posición del primer cliente con un acceso dado
    public int findFirstCustomerEqualsAccess(CustomerType typeCustomer, ArrayList<Metric> listKilbyCosts, ArrayList<Customer> listCustomers) {
        int i = 0;
        boolean found = false;
        CustomerType newTypeCustomer = null;
        int pos = -1;

        while (i < listKilbyCosts.size() && !found) {
            newTypeCustomer = ((CustomerTTRP)getCustomerByID(listKilbyCosts.get(i).getIdElement(), listCustomers)).getTypeCustomer();

            if (newTypeCustomer == typeCustomer) {
                pos = i;
                found = true;
            }

            i++;
        }

        return pos;
    }

    // Método que devuelve el mejor cliente
    public Metric getBestElement(int idDepot, ArrayList<Customer> listElement, ArrayList<Route> listRoutes, double capacityTruck, double capacityTrailer) {
        Metric bestMetricKilby = null;

        double bestCost = 0.0;
        int bestIdElement = -1;
        int bestRoute = -1;
        double currentCost = 0.0;
        double requestRoute = 0.0;
        double requestAnalice = 0.0;
        double totalCapacity = 0.0;
        boolean found = false;
        int i = 0;

        while (i < listElement.size() && !found) {
            if (Problem.getProblem().getTypeProblem() == ProblemType.CVRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.OVRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.HFVRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.OVRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.MDVRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.SBRP
                    || Problem.getProblem().getTypeProblem() == ProblemType.VRPTW
                    || (Problem.getProblem().getTypeProblem() == ProblemType.TTRP
                    && listRoutes.get(0) instanceof RouteTTRP
                    && ((RouteTTRP)listRoutes.get(0)).getTypeRoute() == RouteType.PTR)) {
                totalCapacity = capacityTruck;
            } else {
                totalCapacity = capacityTruck + capacityTrailer;
            }

            int j = 0;
            while (j < listRoutes.size() && !found) {
                if (listRoutes.get(j).getRequestRoute() + listElement.get(i).getRequestCustomer() <= totalCapacity) {
                        boolean twFlag = true;
                        if (typeProblem == ProblemType.VRPTW) {
                            double timeRoute = getTimeRoute(listRoutes.get(j).getListIdCustomers());
                            ArrayList<Customer> feasibleCustomers = get_feasible_customers(listRoutes.get(j).getListIdCustomers().get(listRoutes.get(j).getListIdCustomers().size() - 1));
                            if (listElement.get(i) instanceof CustomerTTRP && feasibleCustomers.contains(listElement.get(i))) {
                                NumericMatrix timeMatrix = Problem.getProblem().getTimeMatrix();
                                double currentTime = timeMatrix.getItem(listRoutes.get(j).getListIdCustomers().get(listRoutes.get(j).getListIdCustomers().size() - 1), listElement.get(i).getIdCustomer());
                                double customerReadyTime = listElement.get(i).getTimeWindow().getInitialNode();
                                double customerServiceTime = listElement.get(i).getTimeWindow().getServiceTime();
                                timeRoute = Math.max(currentTime, customerReadyTime) + customerServiceTime;
                            } else {
                                twFlag = false;
                                bestCost = calculateCostOfKilby(idDepot, listRoutes.get(0).getListIdCustomers().get(0), listElement.get(0).getIdCustomer());
                                j++;
                            }
                        }
                        if (twFlag) {
                            bestIdElement = listElement.get(i).getIdCustomer();
                            bestCost = calculateCostOfKilby(idDepot, listRoutes.get(0).getListIdCustomers().get(0), listElement.get(0).getIdCustomer());
                            bestRoute = j;
                            found = true;
                        }
                    } else {
                        j++;
                    }
            }

            i++;
        }

        for (int k = 0; k < listElement.size(); k++) {
            for (int l = 0; l < listRoutes.size(); l++) {
                if (Problem.getProblem().getTypeProblem() == ProblemType.CVRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.OVRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.HFVRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.OVRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.MDVRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.SBRP
                        || Problem.getProblem().getTypeProblem() == ProblemType.VRPTW
                        || (Problem.getProblem().getTypeProblem() == ProblemType.TTRP
                        && listRoutes.get(l) instanceof RouteTTRP
                        && ((RouteTTRP)listRoutes.get(l)).getTypeRoute() == RouteType.PTR)) {
                    totalCapacity = capacityTruck;
                } else {
                    totalCapacity = capacityTruck + capacityTrailer;
                }

                requestRoute = listRoutes.get(l).getRequestRoute();

                currentCost = calculateCostOfKilby(idDepot, listRoutes.get(l).getListIdCustomers().get(0), listElement.get(k).getIdCustomer());
                    requestAnalice = requestRoute + listElement.get(k).getRequestCustomer();
                

                if (currentCost < bestCost && requestAnalice <= totalCapacity) {
                    bestCost = currentCost;
                    bestIdElement = listElement.get(k).getIdCustomer();
                    
                    bestRoute = l;
                }
            }
        }

        if (found) {
            bestMetricKilby = new Metric();
            bestMetricKilby.setIdElement(bestIdElement);
            bestMetricKilby.setInsertionCost(bestCost);
            bestMetricKilby.setIndex(bestRoute);
        }

        return bestMetricKilby;
    }

    // Método que devuelve la ruta con demanda más cercana a la capacidad
    public int closeRoute(ArrayList<Route> listRoutes) {
        int posRoute = 0;

        double maxCapacity = listRoutes.get(0).getRequestRoute();

        for (int i = 1; i < listRoutes.size(); i++) {
            if (listRoutes.get(i).getRequestRoute() > maxCapacity) {
                maxCapacity = listRoutes.get(i).getRequestRoute();
                posRoute = i;
            }
        }

        return posRoute;
    }

    // Método que determina si una ruta está llena
    public boolean requestPerfect(ArrayList<Customer> elementsToVisit, double capacityTotal, double requestRoute) {
        boolean passVal = false;
        double idealRequest = capacityTotal - requestRoute;

        if (idealRequest != 0) {
            int i = 0;

            while (i < elementsToVisit.size() && !passVal) {
                if (elementsToVisit.get(i).getRequestCustomer() <= idealRequest) {
                        passVal = true;
                    } else {
                        i++;
                    }
                
            }
        }

        return passVal;
    }
    
}
