/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.heuristic;
import cujae.inf.citi.om.data.BusStop;
import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.solution.Route;
import cujae.inf.citi.om.solution.RouteTTRP;
import cujae.inf.citi.om.solution.RouteType;
import cujae.inf.citi.om.solution.Solution;
import cujae.inf.ic.om.matrix.NumericMatrix;
import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.util.Comparator;
import java.util.Map;
import java.util.stream.Collectors;

/**
 *
 * @author nanda
 */

public class MatchingBasedSavingAlgorithm extends Save {

    private ArrayList<Depot> depots;
    private Depot depot;
    private ArrayList<Customer> customers;
    private ArrayList<BusStop> listBusStops;
    private NumericMatrix saveMatrix;
    private ArrayList<Route> listRoutes;
    private ProblemType typeProblem;
    private int idDepot;
    private int posDepot;
    private int cantCustomers;
    private int cantBusStops;
    private boolean repeat;
    private boolean depotFinish;
    private double capacityVehicle;
    private double capacityTrailer;
    private ArrayList<Double> listCapacities;
    private Solution solution;
    private Operator_3opt threeOpt;
    private double timeRoute;
    private ArrayList<Customer> feasibleCustomers;
    private Route currentRoute;
    private boolean existSave;
    private int extInic;
    private int extEnd;

    public MatchingBasedSavingAlgorithm() {
        super();
        this.listRoutes = new ArrayList<>();
        this.solution = new Solution();
        this.threeOpt = new Operator_3opt();
    }

    public void initializeSpecifics() {

        this.depots = Problem.getProblem().getListDepots();
        this.depot = this.depots.get(0);

        if (this.typeProblem == ProblemType.MDVRP) {
            this.customers = Problem.getProblem().getCustomersAssignedByIDDepot(
                this.idDepot, Problem.getProblem().getListCustomers(), this.depots
            );
        } else if (this.typeProblem == ProblemType.SBRP) {
            this.listBusStops = Problem.getProblem().getListBusesStop();
        } else {
            this.customers = Problem.getProblem().getListCustomers();
        }
    }

    public Solution getSolutionInicial() {
        if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP ||
            this.typeProblem == ProblemType.SBRP || this.typeProblem == ProblemType.VRPTW) {
            if (this.typeProblem == ProblemType.SBRP) {
                this.listRoutes = this.matchBasedSavingsAlgorithm(this.listBusStops, this.depots);
            } else {
                this.listRoutes = this.matchBasedSavingsAlgorithm(this.customers, this.depots);
            }

            this.solution.getListRoutes().addAll(this.listRoutes);

        } else if (this.typeProblem == ProblemType.HFVRP) {
            this.listCapacities = new ArrayList<>(Problem.getProblem().getListCapacities());

            while (!this.listRoutes.isEmpty() && !this.listCapacities.isEmpty()) {
                this.listRoutes = this.matchBasedSavingsAlgorithm(this.customers, this.depots);
                this.listCapacities.remove(0);
            }

            this.solution.getListRoutes().addAll(this.listRoutes);

        } else if (this.typeProblem == ProblemType.MDVRP) {
            this.repeat = false;
            this.depotFinish = false;
            for (int j = this.posDepot; j < Problem.getProblem().getListDepots().size(); j++) {
                if (j != this.posDepot) {
                    this.idDepot = Problem.getProblem().getListDepots().get(j).getIdDepot();
                    this.customers = Problem.getProblem().getCustomersAssignedByIDDepot(
                        this.idDepot, Problem.getProblem().getListCustomers(), Problem.getProblem().getListDepots()
                    );

                    this.capacityVehicle = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCapacityVehicle();

                    if (!this.customers.isEmpty()) {
                        this.listRoutes = this.createInitialRoutes(this.customers);
                        this.cantCustomers = this.customers.size();
                        this.saveMatrix = new NumericMatrix(this.cantCustomers, this.cantCustomers);
                        this.saveMatrix = this.fillSaveMatrix(this.idDepot, this.customers);
                    }
                }

                while (!this.listRoutes.isEmpty() && !this.repeat && !this.depotFinish && !this.customers.isEmpty()) {
                    this.listRoutes = this.matchBasedSavingsAlgorithm(this.customers, this.depots);
                    this.cantCustomers = this.customers.size();

                    if (j == (this.depots.size() - 1)) {
                        this.depotFinish = true;
                    }
                }

                this.solution.getListRoutes().addAll(this.listRoutes);
            }

        } else if (this.typeProblem == ProblemType.TTRP) {
            this.capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(this.posDepot).getListFleets().get(0)).getCapacityTrailer();

            while (!this.listRoutes.isEmpty()) {
                this.listRoutes = this.matchBasedSavingsAlgorithm(this.customers, this.depots);
            }

            this.solution.getListRoutes().addAll(this.listRoutes);
        }

        return this.solution;
    }

    public ArrayList<Map.Entry<Map.Entry<Integer, Integer>, Double>> calculateSavingsMatrix(List<?> elements) {
        ArrayList<Map.Entry<Map.Entry<Integer, Integer>, Double>> savingsList = new ArrayList<>();

        for (int i = 0; i < elements.size(); i++) {
            for (int j = i + 1; j < elements.size(); j++) {
                Object c_i = elements.get(i);
                Object c_j = elements.get(j);

                int ci, cj;
                if (this.typeProblem == ProblemType.MDVRP) {
                    ci = Problem.getProblem().getPosElementByIDDepot(this.idDepot, ((Customer) c_i).getIdCustomer());
                    cj = Problem.getProblem().getPosElementByIDDepot(this.idDepot, ((Customer) c_j).getIdCustomer());
                } else {
                    ci = Problem.getProblem().getPosElement(((Customer) c_i).getIdCustomer());
                    cj = Problem.getProblem().getPosElement(((Customer) c_j).getIdCustomer());
                }

                if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP ||
                    this.typeProblem == ProblemType.HFVRP || this.typeProblem == ProblemType.TTRP) {
                    this.posDepot = Problem.getProblem().getPosElement(this.depots.get(0).getIdDepot()) - this.cantCustomers;
                } else {
                    this.posDepot = Problem.getProblem().getPosElement(this.cantCustomers);
                }

                double depotToI = this.saveMatrix.getItem(this.posDepot, ci);
                double depotToJ = this.saveMatrix.getItem(this.posDepot, cj);
                double iToJ = this.saveMatrix.getItem(ci, cj);

                double savings = depotToI + depotToJ - iToJ;

                savingsList.add(new AbstractMap.SimpleEntry<>(
                                new AbstractMap.SimpleEntry<>(((Customer) c_i).getIdCustomer(), ((Customer) c_j).getIdCustomer()),
                                savings));
                
            }
        }

        // Ordenar la lista por el valor de "savings" en orden descendente
        savingsList.sort(Collections.reverseOrder(Comparator.comparingDouble(Map.Entry::getValue)));
        return savingsList;
    }

    public ArrayList<Route> matchBasedSavingsAlgorithm(List<?> elements, List<Depot> depots) {
        if (this.typeProblem == ProblemType.CVRP ||
            this.typeProblem == ProblemType.OVRP || this.typeProblem == ProblemType.HFVRP ||
            this.typeProblem == ProblemType.MDVRP || this.typeProblem == ProblemType.SBRP ||
            this.typeProblem == ProblemType.VRPTW) {

            double fleetCapacity;
            if (this.typeProblem == ProblemType.HFVRP) {
                fleetCapacity = this.listCapacities.get(0);
            } else {
                fleetCapacity = depots.get(0).getListFleets().get(0).getCapacityVehicle();
            }

            ArrayList<Map.Entry<Map.Entry<Integer, Integer>, Double>> savingsList = this.calculateSavingsMatrix(elements);

            for (Map.Entry<Map.Entry<Integer, Integer>, Double> savingTuple : savingsList) {
                Map.Entry<Integer, Integer> customerIds = savingTuple.getKey();
                double saving = savingTuple.getValue();

                Route route1 = null;
                Route route2 = null;

                for (Route route : this.listRoutes) {
                    if (this.typeProblem == ProblemType.SBRP) {
                        if (route.getListBusStops().contains(customerIds.getKey())) {
                            route1 = route;
                        }
                        if (route.getListBusStops().contains(customerIds.getValue())) {
                            route2 = route;
                        }
                    } else {
                        if (route.getListIdCustomers().contains(customerIds.getKey())) {
                            route1 = route;
                        }
                        if (route.getListIdCustomers().contains(customerIds.getValue())) {
                            route2 = route;
                        }
                    }
                }

                if (route1 == null || route2 == null || route1 == route2) {
                    continue;
                }

                double combinedDemand = route1.getRequestRoute() + route2.getRequestRoute();
                if (combinedDemand <= fleetCapacity) {
                    Route mergedRoute;
                    boolean twFlag = true;
                        if (this.typeProblem == ProblemType.VRPTW) {
                            ArrayList<Integer> localR1Ids = new ArrayList<>(route1.getListIdCustomers());
                            ArrayList<Integer> localR2Ids = new ArrayList<>(route2.getListIdCustomers());
                            for (int idCustomer : localR2Ids) {
                                this.timeRoute = this.getTimeRoute(localR1Ids);
                                this.feasibleCustomers = this.get_feasible_customers(localR1Ids.get(localR1Ids.size() - 1));
                                List<Integer> fcIds = new ArrayList<>();
                                for (Customer fc : this.feasibleCustomers) {
                                    fcIds.add(fc.getIdCustomer());
                                }
                                if (fcIds.contains(idCustomer)) {
                                    NumericMatrix timeMatrix = Problem.getProblem().getTimeMatrix();
                                    double currentTime = timeMatrix.getItem(localR1Ids.get(localR1Ids.size() - 1), idCustomer);
                                    Customer customer = Problem.getProblem().getCustomerByIDCustomer(idCustomer);
                                    double customerReadyTime = customer.getTimeWindow().getInitialNode();
                                    double customerServiceTime = customer.getTimeWindow().getServiceTime();
                                    this.timeRoute = Math.max(currentTime, customerReadyTime) + customerServiceTime;
                                } else {
                                    twFlag = false;
                                    break;
                                }
                            }
                        }
                        if (twFlag) {
                            ArrayList<Integer> combinedList = (ArrayList<Integer>) List.of(route1.getListIdCustomers(), route2.getListIdCustomers())
                                .stream()
                                .flatMap(List::stream)
                                .collect(Collectors.toList());
                            mergedRoute = new Route(
                                combinedList,
                                combinedDemand,
                                route1.getCostRoute() + route2.getCostRoute() - saving,
                                depots.get(0).getIdDepot(),
                                null
                            );
                        } else {
                            continue;
                        }
                    

                    this.listRoutes.remove(route1);
                    this.listRoutes.remove(route2);

                    if (this.typeProblem == ProblemType.SBRP) {
                        if (mergedRoute.getListBusStops().size() >= 6) {
                            this.threeOpt.toOptimize(mergedRoute);
                        }
                    } else {
                        if (mergedRoute.getListIdCustomers().size() >= 6) {
                            this.threeOpt.toOptimize(mergedRoute);
                        }
                    }

                    this.listRoutes.add(mergedRoute);

                    if (this.typeProblem == ProblemType.HFVRP) {
                        this.route = mergedRoute;
                        this.updateCustomersToVisit(mergedRoute, this.customersToVisit);
                    }
                }
            }

            if (this.typeProblem == ProblemType.MDVRP) {
                for (Customer c : this.customers) {
                    for (Route r : this.listRoutes) {
                        for (int i = 0; i < r.getListIdCustomers().size(); i++) {
                            if (c.getIdCustomer() == r.getListIdCustomers().get(i)) {
                                this.customers.remove(0);
                            }
                        }
                    }
                }
                List<Route> routesCopy = new ArrayList<>(this.listRoutes);
                if (routesCopy.size() == this.listRoutes.size() && this.depotFinish) {
                    this.repeat = true;
                }
            }
        } else if (this.typeProblem == ProblemType.TTRP) {
            RouteType typeRoute = ((RouteTTRP)this.currentRoute).getTypeRoute();

            if ((typeRoute == RouteType.PTR && this.currentRoute.getRequestRoute() == this.capacityVehicle) ||
                ((typeRoute == RouteType.PVR || typeRoute == RouteType.CVR) &&
                 this.currentRoute.getRequestRoute() == (this.capacityVehicle + this.capacityTrailer))) {

                int extInicPos = Problem.getProblem().getPosElement(this.extInic);
                int extEndPos = Problem.getProblem().getPosElement(this.extEnd);

                for (int i = 0; i < this.saveMatrix.getRowLength(); i++) {
                    this.saveMatrix.setItem(extInicPos, i, Double.NEGATIVE_INFINITY);
                    this.saveMatrix.setItem(i, extInicPos, Double.NEGATIVE_INFINITY);
                    this.saveMatrix.setItem(extEndPos, i, Double.NEGATIVE_INFINITY);
                    this.saveMatrix.setItem(i, extEndPos, Double.NEGATIVE_INFINITY);
                }

                this.existSave = false;
                System.out.println("existSave = False");
                return this.listRoutes;
            }
        }

        return this.listRoutes;
    }

    public void updateCustomersToVisit(Route closeRoute, List<Customer> customersToVisit) {
        for (int i = 0; i < closeRoute.getListIdCustomers().size(); i++) {
            int j = 0;
            boolean found = false;

            while (j < customersToVisit.size() && !found) {
                if (customersToVisit.get(j).getIdCustomer() == closeRoute.getListIdCustomers().get(i)) {
                    customersToVisit.remove(j);
                    found = true;
                } else {
                    j++;
                }
            }
        }
    }
}
