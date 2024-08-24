package cujae.inf.citi.om.tools;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Random;


public class Tools {

	public static double roundDouble(double number, int decimalPlace){
		double numberRound;
		BigDecimal bd = new BigDecimal(number);
		bd = bd.setScale(decimalPlace, BigDecimal.ROUND_UP);
		numberRound = bd.doubleValue();
		return numberRound;
	}

	public static void OrdenateMethod(ArrayList<Double> listCapacities, OrderType typeOrder){
		boolean flag = false;
		
		switch(typeOrder.ordinal())
		{
			case 0: case 1:
			{
				for(int i = 0; i < listCapacities.size() - 1; i++)
				{
					double min = listCapacities.get(i); 
					int pos = i;
	
					for(int j = (i + 1); j < listCapacities.size(); j++)
					{
	
						if(typeOrder.ordinal() == 0)
						{
							if(listCapacities.get(j) <= min)
							{
								min = listCapacities.get(j);
								pos = j;
								
								flag = true;
							}
						}
	
						else
						{
							if(listCapacities.get(j) >= min) 
							{
								min = listCapacities.get(j);
								pos = j;
								
								flag = true;
							}
						}
	
						if(flag)
						{
							listCapacities.set(pos, listCapacities.get(i));
							listCapacities.set(i, min);
							
							flag = false;
						}
					}
				}    
				break;
			}
			case 2:
			{
				Random random = new Random ();
				int index = -1;
	
				ArrayList<Double> listCapacityOrder = new ArrayList<Double>();
	
				int i = 0;
				while(i < listCapacities.size())
				{
					index = random.nextInt(listCapacities.size());
					listCapacityOrder.add(listCapacities.get(index));
					listCapacities.remove(index);
				}
	
				listCapacities.addAll(listCapacityOrder);
				
				break;
			}
		}
	}
}
