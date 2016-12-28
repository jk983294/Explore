package com.victor.lib.commons.collections;

import static org.apache.commons.collections4.functors.EqualPredicate.equalPredicate;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Vector;

import org.apache.commons.collections4.Bag;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.ComparatorUtils;
import org.apache.commons.collections4.Equator;
import org.apache.commons.collections4.Predicate;
import org.apache.commons.collections4.PredicateUtils;
import org.apache.commons.collections4.Transformer;
import org.apache.commons.collections4.TransformerUtils;
import org.apache.commons.collections4.bag.HashBag;
import org.apache.commons.collections4.collection.PredicatedCollection;
import org.apache.commons.collections4.collection.TransformedCollection;
import org.apache.commons.collections4.collection.UnmodifiableCollection;
import org.apache.commons.collections4.functors.DefaultEquator;
import org.apache.commons.collections4.queue.CircularFifoQueue;
import org.junit.Before;
import org.junit.Test;

/**
 * Tests for CollectionUtils.
 */
@SuppressWarnings("boxing")
public class CollectionUtilsTest  {

    /**
     * Collection of {@link Integer}s
     */
    private List<Integer> collectionA = null;

    /**
     * Collection of {@link Long}s
     */
    private List<Long> collectionB = null;

    /**
     * Collection of {@link Integer}s that are equivalent to the Longs in
     * collectionB.
     */
    private Collection<Integer> collectionC = null;

    /**
     * Sorted Collection of {@link Integer}s
     */
    private Collection<Integer> collectionD = null;

    /**
     * Sorted Collection of {@link Integer}s
     */
    private Collection<Integer> collectionE = null;

    /**
     * Collection of {@link Integer}s, bound as {@link Number}s
     */
    private Collection<Number> collectionA2 = null;

    /**
     * Collection of {@link Long}s, bound as {@link Number}s
     */
    private Collection<Number> collectionB2 = null;

    /**
     * Collection of {@link Integer}s (cast as {@link Number}s) that are
     * equivalent to the Longs in collectionB.
     */
    private Collection<Number> collectionC2 = null;

    private Iterable<Integer> iterableA = null;

    private Iterable<Long> iterableB = null;

    private Iterable<Integer> iterableC = null;

    private Iterable<Number> iterableA2 = null;

    private Iterable<Number> iterableB2 = null;

    private Collection<Integer> emptyCollection = new ArrayList<>(1);

    @Before
    public void setUp() {
        collectionA = new ArrayList<>();
        collectionA.add(1);
        collectionA.add(2);
        collectionA.add(2);
        collectionA.add(3);
        collectionA.add(3);
        collectionA.add(3);
        collectionA.add(4);
        collectionA.add(4);
        collectionA.add(4);
        collectionA.add(4);
        collectionB = new LinkedList<>();
        collectionB.add(5L);
        collectionB.add(4L);
        collectionB.add(4L);
        collectionB.add(3L);
        collectionB.add(3L);
        collectionB.add(3L);
        collectionB.add(2L);
        collectionB.add(2L);
        collectionB.add(2L);
        collectionB.add(2L);

        collectionC = new ArrayList<>();
        for (final Long l : collectionB) {
            collectionC.add(l.intValue());
        }

        iterableA = collectionA;
        iterableB = collectionB;
        iterableC = collectionC;
        collectionA2 = new ArrayList<>(collectionA);
        collectionB2 = new LinkedList<>(collectionB);
        collectionC2 = new LinkedList<>(collectionC);
        iterableA2 = collectionA2;
        iterableB2 = collectionB2;

        collectionD = new ArrayList<>();
        collectionD.add(1);
        collectionD.add(3);
        collectionD.add(3);
        collectionD.add(3);
        collectionD.add(5);
        collectionD.add(7);
        collectionD.add(7);
        collectionD.add(10);

        collectionE = new ArrayList<>();
        collectionE.add(2);
        collectionE.add(4);
        collectionE.add(4);
        collectionE.add(5);
        collectionE.add(6);
        collectionE.add(6);
        collectionE.add(9);
    }

    @Test
    public void getCardinalityMap() {
        final Map<Number, Integer> freqA = CollectionUtils.<Number>getCardinalityMap(iterableA);
        assertEquals(1, (int) freqA.get(1));
        assertNull(freqA.get(5));
    }

    @Test
    public void cardinality() {
        assertEquals(1, CollectionUtils.cardinality(1, iterableA));
        assertEquals(4, CollectionUtils.cardinality(2L, iterableB));
        assertEquals(0, CollectionUtils.cardinality(2L, iterableA2));

        final Set<String> set = new HashSet<>();
        set.add("A");
        set.add("C");
        set.add("E");
        set.add("E");
        assertEquals(1, CollectionUtils.cardinality("A", set));

        final Bag<String> bag = new HashBag<>();
        bag.add("A", 3);
        bag.add("C");
        bag.add("E");
        bag.add("E");
        assertEquals(3, CollectionUtils.cardinality("A", bag));
    }

    @Test
    public void cardinalityOfNull() {
        final List<String> list = new ArrayList<>();
        assertEquals(0, CollectionUtils.cardinality(null, list));
    }

    @Test
    public void containsAll() {
        final Collection<String> one = new ArrayList<>(1);
        one.add("1");
        final Collection<String> odds = new ArrayList<>(2);
        odds.add("1");
        odds.add("3");
        assertTrue("containsAll({1},{1,3}) should return false.", !CollectionUtils.containsAll(one, odds));
        assertTrue("containsAll({1,3},{1}) should return true.", CollectionUtils.containsAll(odds, one));
    }

    @Test
    public void containsAny() {
        final Collection<String> one = new ArrayList<>(1);
        one.add("1");
        final Collection<String> odds = new ArrayList<>(2);
        odds.add("1");
        odds.add("3");

        assertTrue("containsAny({1},{1,3}) should return true.", CollectionUtils.containsAny(one, odds));
        assertTrue("containsAny({1,3},{1}) should return true.", CollectionUtils.containsAny(odds, one));
    }

    @Test
    public void testSubtract() {
        final Collection<Integer> col = CollectionUtils.subtract(iterableA, iterableC);
        final Map<Integer, Integer> freq = CollectionUtils.getCardinalityMap(col);
        assertEquals(Integer.valueOf(1), freq.get(1));
        assertNull(freq.get(2));
        assertNull(freq.get(3));
        assertEquals(Integer.valueOf(2), freq.get(4));
        assertNull(freq.get(5));

        final Collection<Number> col2 = CollectionUtils.subtract(collectionC2, collectionA);
        final Map<Number, Integer> freq2 = CollectionUtils.getCardinalityMap(col2);
        assertEquals(Integer.valueOf(1), freq2.get(5));
        assertNull(freq2.get(4));
        assertNull(freq2.get(3));
        assertEquals(Integer.valueOf(2), freq2.get(2));
        assertNull(freq2.get(1));
    }

    @Test
    public void testSubtractWithPredicate() {
        // greater than 3
        final Predicate<Number> predicate = new Predicate<Number>() {
            public boolean evaluate(final Number n) {
                return n.longValue() > 3L;
            }
        };

        final Collection<Number> col = CollectionUtils.subtract(iterableA, collectionC, predicate);
        final Map<Number, Integer> freq2 = CollectionUtils.getCardinalityMap(col);
        assertEquals(Integer.valueOf(1), freq2.get(1));
    }

    @Test
    public void testIsSubCollectionOfSelf() {
        assertTrue(CollectionUtils.isSubCollection(collectionA, collectionA));
        assertTrue(CollectionUtils.isSubCollection(collectionB, collectionB));
    }

    @Test
    public void testIsEqualCollection() {
        assertTrue(!CollectionUtils.isEqualCollection(collectionA, collectionC));
        assertTrue(!CollectionUtils.isEqualCollection(collectionC, collectionA));
    }

    @Test
    public void testIsEqualCollectionEquator() {
        // odd / even equator
        final Equator<Integer> e = new Equator<Integer>() {
            public boolean equate(final Integer o1, final Integer o2) {
                if (o1.intValue() % 2 == 0 ^ o2.intValue() % 2 == 0) {
                    return false;
                } else {
                    return true;
                }
            }

            public int hash(final Integer o) {
                return o.intValue() % 2 == 0 ? Integer.valueOf(0).hashCode() : Integer.valueOf(1).hashCode();
            }
        };
        assertTrue(CollectionUtils.isEqualCollection(collectionA, collectionA, e));

        final Equator<Number> defaultEquator = DefaultEquator.defaultEquator();
        assertFalse(CollectionUtils.isEqualCollection(collectionA, collectionB, defaultEquator));
    }

    @Test(expected=IllegalArgumentException.class)
    public void testIsEqualCollectionNullEquator() {
        CollectionUtils.isEqualCollection(collectionA, collectionA, null);
    }

    @Test
    public void find() {
        Predicate<Number> testPredicate = equalPredicate((Number) 4);
        Integer test = CollectionUtils.find(collectionA, testPredicate);
        assertTrue(test.equals(4));
        testPredicate = equalPredicate((Number) 45);
        test = CollectionUtils.find(collectionA, testPredicate);
        assertTrue(test == null);
        assertNull(CollectionUtils.find(null,testPredicate));
        assertNull(CollectionUtils.find(collectionA, null));
    }

    @Test
    public void getFromMap() {
        // Unordered map, entries exist
        final Map<String, String> expected = new HashMap<>();
        expected.put("zeroKey", "zero");
        expected.put("oneKey", "one");

        final Map<String, String> found = new HashMap<>();
        Map.Entry<String, String> entry = CollectionUtils.get(expected, 0);
        found.put(entry.getKey(), entry.getValue());
        entry = CollectionUtils.get(expected, 1);
        found.put(entry.getKey(), entry.getValue());
        assertEquals(expected, found);

        // Map index out of range
        try {
            CollectionUtils.get(expected, 2);
            fail("Expecting IndexOutOfBoundsException.");
        } catch (final IndexOutOfBoundsException e) {
            // expected
        }
        try {
            CollectionUtils.get(expected, -2);
            fail("Expecting IndexOutOfBoundsException.");
        } catch (final IndexOutOfBoundsException e) {
            // expected
        }

        // Sorted map, entries exist, should respect order
        final SortedMap<String, String> map = new TreeMap<>();
        map.put("zeroKey", "zero");
        map.put("oneKey", "one");
        Map.Entry<String, String> test = CollectionUtils.get(map, 1);
        assertEquals("zeroKey", test.getKey());
        assertEquals("zero", test.getValue());
        test = CollectionUtils.get(map, 0);
        assertEquals("oneKey", test.getKey());
        assertEquals("one", test.getValue());
    }

    @Test
    public void getFromIterator() throws Exception {
        // Iterator, entry exists
        Iterator<Integer> iterator = iterableA.iterator();
        assertEquals(1, (int) CollectionUtils.get(iterator, 0));
        iterator = iterableA.iterator();
        assertEquals(2, (int) CollectionUtils.get(iterator, 1));

        // Iterator, non-existent entry
        try {
            CollectionUtils.get(iterator, 10);
            fail("Expecting IndexOutOfBoundsException.");
        } catch (final IndexOutOfBoundsException e) {
            // expected
        }
        assertTrue(!iterator.hasNext());
    }

    @Test
    public void getFromEnumeration() throws Exception {
        // Enumeration, entry exists
        final Vector<String> vector = new Vector<>();
        vector.addElement("zero");
        vector.addElement("one");
        Enumeration<String> en = vector.elements();
        assertEquals("zero", CollectionUtils.get(en, 0));
        en = vector.elements();
        assertEquals("one", CollectionUtils.get(en, 1));

        // Enumerator, non-existent entry
        try {
            CollectionUtils.get(en, 3);
            fail("Expecting IndexOutOfBoundsException.");
        } catch (final IndexOutOfBoundsException e) {
            // expected
        }
        assertTrue(!en.hasMoreElements());
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void getFromPrimitiveArray() throws Exception {
        // Primitive array, entry exists
        final int[] array = new int[2];
        array[0] = 10;
        array[1] = 20;
        assertEquals(10, CollectionUtils.get(array, 0));
        assertEquals(20, CollectionUtils.get(array, 1));

        // Object array, non-existent entry --
        // ArrayIndexOutOfBoundsException
        CollectionUtils.get(array, 2);
    }

    // -----------------------------------------------------------------------
    @Test
    public void testSizeIsEmpty_Null() {
        assertEquals(true, CollectionUtils.sizeIsEmpty(null));
    }

    @Test
    public void testSizeIsEmpty_List() {
        final List<String> list = new ArrayList<>();
        assertEquals(true, CollectionUtils.sizeIsEmpty(list));
        list.add("a");
        assertEquals(false, CollectionUtils.sizeIsEmpty(list));
    }

    @Test
    public void testSizeIsEmpty_Map() {
        final Map<String, String> map = new HashMap<>();
        assertEquals(true, CollectionUtils.sizeIsEmpty(map));
        map.put("1", "a");
        assertEquals(false, CollectionUtils.sizeIsEmpty(map));
    }

    @Test
    public void testSizeIsEmpty_Array() {
        final Object[] objectArray = new Object[0];
        assertEquals(true, CollectionUtils.sizeIsEmpty(objectArray));

        final String[] stringArray = new String[3];
        assertEquals(false, CollectionUtils.sizeIsEmpty(stringArray));
        stringArray[0] = "a";
        stringArray[1] = "b";
        stringArray[2] = "c";
        assertEquals(false, CollectionUtils.sizeIsEmpty(stringArray));
    }

    @Test
    public void testSizeIsEmpty_PrimitiveArray() {
        final int[] intArray = new int[0];
        assertEquals(true, CollectionUtils.sizeIsEmpty(intArray));

        final double[] doubleArray = new double[3];
        assertEquals(false, CollectionUtils.sizeIsEmpty(doubleArray));
        doubleArray[0] = 0.0d;
        doubleArray[1] = 1.0d;
        doubleArray[2] = 2.5d;
        assertEquals(false, CollectionUtils.sizeIsEmpty(doubleArray));
    }

    @Test
    public void testSizeIsEmpty_Enumeration() {
        final Vector<String> list = new Vector<>();
        assertEquals(true, CollectionUtils.sizeIsEmpty(list.elements()));
        list.add("a");
        assertEquals(false, CollectionUtils.sizeIsEmpty(list.elements()));
        final Enumeration<String> en = list.elements();
        en.nextElement();
        assertEquals(true, CollectionUtils.sizeIsEmpty(en));
    }

    @Test
    public void testSizeIsEmpty_Iterator() {
        final List<String> list = new ArrayList<>();
        assertEquals(true, CollectionUtils.sizeIsEmpty(list.iterator()));
        list.add("a");
        assertEquals(false, CollectionUtils.sizeIsEmpty(list.iterator()));
        final Iterator<String> it = list.iterator();
        it.next();
        assertEquals(true, CollectionUtils.sizeIsEmpty(it));
    }
    
    // -----------------------------------------------------------------------
    private static Predicate<Number> EQUALS_TWO = new Predicate<Number>() {
        public boolean evaluate(final Number input) {
            return input.intValue() == 2;
        }
    };

//Up to here
    @Test
    public void filter() {
        final List<Integer> ints = new ArrayList<>();
        ints.add(1);
        ints.add(2);
        ints.add(3);
        ints.add(3);
        final Iterable<Integer> iterable = ints;
        assertTrue(CollectionUtils.filter(iterable, EQUALS_TWO));
        assertEquals(1, ints.size());
        assertEquals(2, (int) ints.get(0));
    }

    @Test
    public void filterNullParameters() throws Exception {
        final List<Long> longs = Collections.nCopies(4, 10L);
        assertFalse(CollectionUtils.filter(longs, null));
        assertEquals(4, longs.size());
    }

    @Test
    public void filterInverse() {
        final List<Integer> ints = new ArrayList<>();
        ints.add(1);
        ints.add(2);
        ints.add(3);
        ints.add(3);
        final Iterable<Integer> iterable = ints;
        assertTrue(CollectionUtils.filterInverse(iterable, EQUALS_TWO));
        assertEquals(3, ints.size());
        assertEquals(1, (int) ints.get(0));
        assertEquals(3, (int) ints.get(1));
        assertEquals(3, (int) ints.get(2));
    }

    @Test
    public void countMatches() {
        assertEquals(4, CollectionUtils.countMatches(iterableB, EQUALS_TWO));
        assertEquals(0, CollectionUtils.countMatches(iterableA, null));
        assertEquals(0, CollectionUtils.countMatches(null, EQUALS_TWO));
        assertEquals(0, CollectionUtils.countMatches(null, null));
    }

    @Test
    public void exists() {
        final List<Integer> list = new ArrayList<>();
        list.add(4);
        assertFalse(CollectionUtils.exists(list, EQUALS_TWO));
        list.add(2);
        assertEquals(true, CollectionUtils.exists(list, EQUALS_TWO));
    }

    @Test
    public void select() {
        final List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        list.add(4);
        // Ensure that the collection is the input type or a super type
        final Collection<Integer> output1 = CollectionUtils.select(list, EQUALS_TWO);
        final Collection<Number> output2 = CollectionUtils.<Number>select(list, EQUALS_TWO);
        final HashSet<Number> output3 = CollectionUtils.select(list, EQUALS_TWO, new HashSet<>());
        assertTrue(CollectionUtils.isEqualCollection(output1, output3));
        assertEquals(4, list.size());
        assertEquals(1, output1.size());
        assertEquals(2, output2.iterator().next());
    }

    @Test
    public void selectRejected() {
        final List<Long> list = new ArrayList<>();
        list.add(1L);
        list.add(2L);
        list.add(3L);
        list.add(4L);
        final Collection<Long> output1 = CollectionUtils.selectRejected(list, EQUALS_TWO);
        final Collection<? extends Number> output2 = CollectionUtils.selectRejected(list, EQUALS_TWO);
        final HashSet<Number> output3 = CollectionUtils.selectRejected(list, EQUALS_TWO, new HashSet<>());
        assertTrue(CollectionUtils.isEqualCollection(output1, output2));
        assertTrue(CollectionUtils.isEqualCollection(output1, output3));
        assertEquals(4, list.size());
        assertEquals(3, output1.size());
        assertTrue(output1.contains(1L));
        assertTrue(output1.contains(3L));
        assertTrue(output1.contains(4L));
    }

    @Test
    public void collect() {
        final Transformer<Number, Long> transformer = TransformerUtils.constantTransformer(2L);
        Collection<Number> collection = CollectionUtils.<Integer, Number>collect(iterableA, transformer);
        assertTrue(collection.size() == collectionA.size());

        ArrayList<Number> list;
        list = CollectionUtils.collect(collectionA, transformer, new ArrayList<>());
        assertTrue(list.size() == collectionA.size());

        Iterator<Integer> iterator = null;
        list = CollectionUtils.collect(iterator, transformer, new ArrayList<>());

        iterator = collectionA.iterator();
        collection = CollectionUtils.<Integer, Number>collect(iterator, transformer);
        assertTrue(collection.size() == collectionA.size());
        assertTrue(collection.contains(2L) && !collection.contains(1));
        collection = CollectionUtils.collect((Iterator<Integer>) null, (Transformer<Integer, Number>) null);
        assertTrue(collection.size() == 0);

        final int size = collectionA.size();
        collectionB = CollectionUtils.collect((Collection<Integer>) null, transformer, collectionB);
        assertTrue(collectionA.size() == size && collectionA.contains(1));
    }

    Transformer<Object, Integer> TRANSFORM_TO_INTEGER = new Transformer<Object, Integer>() {
        public Integer transform(final Object input) {
            return Integer.valueOf(((Long)input).intValue());
        }
    };

    @Test
    public void transform1() {
        List<Number> list = new ArrayList<>();
        list.add(1L);
        list.add(2L);
        list.add(3L);
        CollectionUtils.transform(list, TRANSFORM_TO_INTEGER);
        assertEquals(1, list.get(0));

        list = new ArrayList<>();
        list.add(1L);
        list.add(2L);
        list.add(3L);
        CollectionUtils.transform(null, TRANSFORM_TO_INTEGER);
        assertEquals(3, list.size());
    }

    @Test
    public void transform2() {
        final Set<Number> set = new HashSet<>();
        set.add(1L);
        set.add(2L);
        set.add(3L);
        CollectionUtils.transform(set, new Transformer<Object, Integer>() {
            public Integer transform(final Object input) {
                return 4;
            }
        });
        assertEquals(1, set.size());
        assertEquals(4, set.iterator().next());
    }

    // -----------------------------------------------------------------------
    @Test
    public void addIgnoreNull() {
        final Set<String> set = new HashSet<>();
        set.add("1");
        set.add("2");
        set.add("3");
        assertFalse(CollectionUtils.addIgnoreNull(set, null));
        assertEquals(3, set.size());
        assertFalse(CollectionUtils.addIgnoreNull(set, "1"));
        assertEquals(3, set.size());
        assertEquals(true, CollectionUtils.addIgnoreNull(set, "4"));
        assertEquals(4, set.size());
        assertEquals(true, set.contains("4"));
    }

    // -----------------------------------------------------------------------
    @Test
    public void predicatedCollection() {
        final Predicate<Object> predicate = PredicateUtils.instanceofPredicate(Integer.class);
        Collection<Number> collection = CollectionUtils.predicatedCollection(new ArrayList<>(), predicate);
        assertTrue("returned object should be a PredicatedCollection", collection instanceof PredicatedCollection);
        try {
            CollectionUtils.predicatedCollection(new ArrayList<>(), null);
            fail("Expecting IllegalArgumentException for null predicate.");
        } catch (final IllegalArgumentException ex) {
            // expected
        }
        try {
            CollectionUtils.predicatedCollection(null, predicate);
            fail("Expecting IllegalArgumentException for null collection.");
        } catch (final IllegalArgumentException ex) {
            // expected
        }
    }

    @Test
    public void isFull() {
        final Set<String> set = new HashSet<>();
        set.add("1");
        set.add("2");
        set.add("3");
        final CircularFifoQueue<String> buf = new CircularFifoQueue<>(set);
        assertEquals(false, CollectionUtils.isFull(buf));
        buf.remove("2");
        assertFalse(CollectionUtils.isFull(buf));
        buf.add("2");
        assertEquals(false, CollectionUtils.isFull(buf));
    }

    @Test
    public void maxSize() {
        final Set<String> set = new HashSet<>();
        set.add("1");
        set.add("2");
        set.add("3");
        final Queue<String> buf = new CircularFifoQueue<>(set);
        assertEquals(3, CollectionUtils.maxSize(buf));
        buf.remove("2");
        assertEquals(3, CollectionUtils.maxSize(buf));
        buf.add("2");
        assertEquals(3, CollectionUtils.maxSize(buf));
    }

    // -----------------------------------------------------------------------
    //Up to here
    @Test
    public void testRetainAll() {
        final List<String> base = new ArrayList<>();
        base.add("A");
        base.add("B");
        base.add("C");
        final List<Object> sub = new ArrayList<>();
        sub.add("A");
        sub.add("C");
        sub.add("X");

        final Collection<String> result = CollectionUtils.retainAll(base, sub);
    }

    @Test
    public void testRemoveAll() {
        final List<String> base = new ArrayList<>();
        base.add("A");
        base.add("B");
        base.add("C");
        final List<String> sub = new ArrayList<>();
        sub.add("A");
        sub.add("C");
        sub.add("X");

        final Collection<String> result = CollectionUtils.removeAll(base, sub);
    }

    // -----------------------------------------------------------------------
    @Test
    public void testTransformedCollection() {
        final Transformer<Object, Object> transformer = TransformerUtils.nopTransformer();
        Collection<Object> collection = CollectionUtils.transformingCollection(new ArrayList<>(), transformer);
        assertTrue("returned object should be a TransformedCollection", collection instanceof TransformedCollection);
    }

    @Test
    public void testTransformedCollection_2() {
        final List<Object> list = new ArrayList<>();
        list.add("1");
        list.add("2");
        list.add("3");
        final Collection<Object> result = CollectionUtils.transformingCollection(list, TRANSFORM_TO_INTEGER);
        assertEquals(true, result.contains("1")); // untransformed
        assertEquals(true, result.contains("2")); // untransformed
        assertEquals(true, result.contains("3")); // untransformed
    }

    @Test
    public void testUnmodifiableCollection() {
        Collection<Object> col = CollectionUtils.unmodifiableCollection(new ArrayList<>());
        assertTrue("Returned object should be a UnmodifiableCollection.", col instanceof UnmodifiableCollection);
    }

    @Test
    public void emptyCollection() throws Exception {
        final Collection<Number> coll = CollectionUtils.emptyCollection();
        assertEquals(CollectionUtils.EMPTY_COLLECTION, coll);
    }

    @Test
    public void emptyIfNull() {
        assertTrue(CollectionUtils.emptyIfNull(null).isEmpty());
        final Collection<Object> collection = new ArrayList<>();
        assertSame(collection, CollectionUtils.emptyIfNull(collection));
    }

    @Test
    public void get() {
        assertEquals(2, CollectionUtils.get((Object)collectionA, 2));
        assertEquals(2, CollectionUtils.get((Object)collectionA.iterator(), 2));
        final Map<Integer, Integer> map = CollectionUtils.getCardinalityMap(collectionA);
        assertEquals(map.entrySet().iterator().next(), CollectionUtils.get((Object)map, 0));
    }

    @Test
    public void reverse() {
        CollectionUtils.reverseArray(new Object[] {});
        final Integer[] a = collectionA.toArray(new Integer[collectionA.size()]);
        CollectionUtils.reverseArray(a);
        // assume our implementation is correct if it returns the same order as the Java function
        Collections.reverse(collectionA);
        assertEquals(collectionA, Arrays.asList(a));
    }

    @Test(expected=IllegalArgumentException.class)
    public void collateException1() {
        CollectionUtils.collate(collectionA, null);
    }

    @Test(expected=IllegalArgumentException.class)
    public void collateException2() {
        CollectionUtils.collate(collectionA, collectionC, null);
    }

    @Test
    public void testCollate() {
        List<Integer> result = CollectionUtils.collate(emptyCollection, emptyCollection);
        assertEquals("Merge empty with empty", 0, result.size());

        result = CollectionUtils.collate(collectionA, emptyCollection);
        assertEquals("Merge empty with non-empty", collectionA, result);

        List<Integer> result1 = CollectionUtils.collate(collectionD, collectionE);
        List<Integer> result2 = CollectionUtils.collate(collectionE, collectionD);
        assertEquals("Merge two lists 1", result1, result2);

        List<Integer> combinedList = new ArrayList<>();
        combinedList.addAll(collectionD);
        combinedList.addAll(collectionE);
        Collections.sort(combinedList);

        assertEquals("Merge two lists 2", combinedList, result2);

        final Comparator<Integer> reverseComparator =
                ComparatorUtils.reversedComparator(ComparatorUtils.<Integer>naturalComparator());

        result = CollectionUtils.collate(emptyCollection, emptyCollection, reverseComparator);
        assertEquals("Comparator Merge empty with empty", 0, result.size());

        Collections.reverse((List<Integer>) collectionD);
        Collections.reverse((List<Integer>) collectionE);
        Collections.reverse(combinedList);

        result1 = CollectionUtils.collate(collectionD, collectionE, reverseComparator);
        result2 = CollectionUtils.collate(collectionE, collectionD, reverseComparator);
        assertEquals("Comparator Merge two lists 1", result1, result2);
        assertEquals("Comparator Merge two lists 2", combinedList, result2);
    }

    @Test
    public void testCollateIgnoreDuplicates() {
        List<Integer> result1 = CollectionUtils.collate(collectionD, collectionE, false);
        List<Integer> result2 = CollectionUtils.collate(collectionE, collectionD, false);
        assertEquals("Merge two lists 1 - ignore duplicates", result1, result2);

        Set<Integer> combinedSet = new HashSet<>();
        combinedSet.addAll(collectionD);
        combinedSet.addAll(collectionE);
        List<Integer> combinedList = new ArrayList<>(combinedSet);
        Collections.sort(combinedList);

        assertEquals("Merge two lists 2 - ignore duplicates", combinedList, result2);
    }

    @Test
    public void testPermutations() {
        List<Integer> sample = collectionA.subList(0, 5);
        Collection<List<Integer>> permutations = CollectionUtils.permutations(sample);

        // result size = n!
        int collSize = sample.size();
        int factorial = 1;
        for (int i = 1; i <= collSize; i++) {
            factorial *= i;
        }
        assertEquals(factorial, permutations.size());
    }

    @Test
    public void testMatchesAll() {
        Predicate<Integer> lessThanFive = new Predicate<Integer>() {
            public boolean evaluate(Integer object) {
                return object < 5;
            }
        };
        assertTrue(CollectionUtils.matchesAll(collectionA, lessThanFive));

        Predicate<Integer> lessThanFour = new Predicate<Integer>() {
            public boolean evaluate(Integer object) {
                return object < 4;
            }
        };
        assertFalse(CollectionUtils.matchesAll(collectionA, lessThanFour));

        assertTrue(CollectionUtils.matchesAll(null, lessThanFour));
        assertTrue(CollectionUtils.matchesAll(emptyCollection, lessThanFour));
    }
}
