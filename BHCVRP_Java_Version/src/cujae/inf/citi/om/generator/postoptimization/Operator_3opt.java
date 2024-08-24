package cujae.inf.citi.om.generator.postoptimization;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import cujae.inf.citi.om.generator.solution.Route;

/* Clase que implementa el operador 3-opt */

public class Operator_3opt extends StepOptimization{

	@Override
	public void toOptimize(Route route) {
		// TODO Auto-generated method stub
		ArrayList<Integer> listOpt = new ArrayList<Integer>(route.getListIdCustomers());
		ArrayList<Integer> listAux = new ArrayList<Integer>(route.getListIdCustomers());
		ArrayList<Integer> listKey = new ArrayList<Integer>();

		double bestCost = route.getCostSingleRoute();
		double currentCost = 0.0;
		
		Random random = new Random ();
		int keyFirst = random.nextInt(route.getListIdCustomers().size());
		int keySecond = random.nextInt(route.getListIdCustomers().size());
		int keyThird = random.nextInt(route.getListIdCustomers().size());	

		if(route.getListIdCustomers().size() > 5){
                    while((keyFirst == keySecond)||(keyFirst == keyThird)||(keySecond == keyThird)||(Math.abs(keyFirst - keySecond) <= 1)||(Math.abs(keyFirst - keyThird) <= 1)||(Math.abs(keySecond - keyThird) <= 1)
			||((keyFirst == route.getListIdCustomers().size()-1) && (keySecond == 0 || keyThird == 0))
			||((keySecond == route.getListIdCustomers().size()-1) && (keyFirst == 0 || keyThird == 0))
			||((keyThird == route.getListIdCustomers().size()-1) && (keySecond == 0 || keyFirst == 0)))
                    {
                            keyFirst = random.nextInt(route.getListIdCustomers().size());
                            keySecond = random.nextInt(route.getListIdCustomers().size());
                            keyThird = random.nextInt(route.getListIdCustomers().size());	
                    }
                    
                }
                

		if(((Math.min(keyFirst, keySecond)) == keyFirst) && ((Math.min(keyFirst, keyThird)) == keyFirst))
		{
			listKey.add(keyFirst);
			listKey.add((Math.min(keySecond, keyThird)));
			listKey.add((Math.max(keySecond, keyThird)));
		}

		if(((Math.min(keySecond, keyFirst)) == keySecond) && ((Math.min(keySecond, keyThird)) == keySecond))
		{
			listKey.add(keySecond);
			listKey.add((Math.min(keyFirst, keyThird)));
			listKey.add((Math.max(keyFirst, keyThird)));
		}
		
		if(((Math.min(keyThird, keyFirst)) == keyThird) && ((Math.min(keyThird, keySecond)) == keyThird))
		{
			listKey.add(keyThird);
			listKey.add((Math.min(keyFirst, keySecond)));
			listKey.add((Math.max(keyFirst, keySecond)));
		}

		ArrayList<Integer> listCandidates;
		
		int moves = 0;
		while(moves < 7)
		{
			listCandidates = new ArrayList<Integer>(listAux);
				
			switch(moves)
			{
				case 0:
				{
					Invert(listCandidates, listKey.get(1), listKey.get(2));
					route.setListIdCustomers(listCandidates);
					listKey.add(listKey.remove(0));
		
					break;	
				}
				
				case 1:
				{
					Invert(listCandidates, listKey.get(1), listKey.get(2));
					listKey.add(listKey.remove(0));
		
					route.setListIdCustomers(listCandidates);
		
					break;	
				}
				
				case 2:
				{
					Invert(listCandidates, listKey.get(1), listKey.get(2));
					listKey.add(listKey.remove(0));
		
					route.setListIdCustomers(listCandidates);
		
					break;	
				}
				
				case 3:
				{
					Invert(listCandidates, listKey.get(0), listKey.get(1));
					Invert(listCandidates,  listKey.get(1),  listKey.get(2));
		
					route.setListIdCustomers(listCandidates);
		
					break;
				}
				
				case 4:
				{
					List<Integer> cadOne = listCandidates.subList((listKey.get(0) + 1), (listKey.get(1) + 1));
					List<Integer> cadTwo = listCandidates.subList((listKey.get(1) + 1), (listKey.get(2) + 1));
		
					int posInsertOne =  listKey.get(0) + 1;
					int posInsertTwo =  listKey.get(0) + cadTwo.size() + 1;
		
					listCandidates = Swap(listCandidates, cadOne, cadTwo, posInsertOne, posInsertTwo);
		
					route.setListIdCustomers(listCandidates);
		
					break;
				}
				
				case 5:
				{
					List<Integer> cadOne = listCandidates.subList((listKey.get(0) + 1), (listKey.get(1) + 1));
					List<Integer> cadTwo = listCandidates.subList((listKey.get(1) + 1), (listKey.get(2) + 1));
		
					int posInsertOne = listKey.get(0) + 1;
					int posInsertTwo = listKey.get(0) + cadTwo.size() + 1;
		
					Invert(listCandidates, listKey.get(0), listKey.get(1));
					cadOne =  listCandidates.subList((listKey.get(0) + 1), (listKey.get(1) + 1));
					listCandidates = Swap(listCandidates, cadOne, cadTwo, posInsertOne, posInsertTwo);
		
					route.setListIdCustomers(listCandidates);
		
					break;
				}
				
				case 6:
				{
					List<Integer> cadOne = listCandidates.subList((listKey.get(0) + 1), (listKey.get(1) + 1));
					List<Integer> cadTwo = listCandidates.subList((listKey.get(1) + 1), (listKey.get(2) + 1));
		
					int posInsertOne = listKey.get(0) + 1;
					int posInsertTwo = listKey.get(0) + cadTwo.size() + 1;
		
					Invert(listCandidates, listKey.get(1), listKey.get(2));
					cadTwo = listCandidates.subList((listKey.get(1) + 1), (listKey.get(2) + 1));
					listCandidates = Swap(listCandidates, cadOne, cadTwo, posInsertOne, posInsertTwo);
		
					route.setListIdCustomers(listCandidates);
		
					break;
				}
			}
			
			currentCost = route.getCostSingleRoute();

			if(bestCost > currentCost)
			{
				bestCost = currentCost;
				listOpt = new ArrayList<Integer>(listCandidates);
			}
			
			moves++;
		}	
		
		route.setListIdCustomers(listOpt);
		route.setCostRoute(bestCost);
	}

	
	/* Metodo que intercambia dos cadenas */
	public ArrayList<Integer> Swap(ArrayList<Integer> listCandidates, List<Integer> cadOne, List<Integer> cadTwo, int posInsertOne, int posInsertTwo){
		ArrayList<Integer> listTemp = new ArrayList<Integer>();

		for(int i = 0; i < listCandidates.size(); i++)
		{
			if(i == posInsertOne)
			{
				for(int j = 0; j < cadTwo.size(); j++)
				{
					listTemp.add(i, cadTwo.get(j));
					i++;
				}
			}
			
			if(i == posInsertTwo)
			{
				for(int j = 0; j < cadOne.size(); j++)
				{
					listTemp.add(i, cadOne.get(j)); 
					i++;
				}
				
				i--;
			}

			else
				listTemp.add(listCandidates.get(i));
		}
		
		return listTemp;
	}
}
